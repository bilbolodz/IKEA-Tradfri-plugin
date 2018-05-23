# Goolgle Home page example
#
# Author: Dnpwwo, 2017
#
#   Demonstrates HTTP connectivity.
#   After connection it performs a GET on  www.google.com and receives a 302 (Page Moved) response
#   It then does a subsequent GET on the Location specified in the 302 response and receives a 200 response.
#
"""
<plugin key="IKEA-Tradfri" name="IKEA Tradfri" author="moroen" version="1.0" externallink="https://github.com/moroen/IKEA-Tradfri-plugin">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="localhost"/>
        <param field="Port" label="Port" width="30px" required="true" default="8085"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
                <option label="Logging" value="File"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import json

class BasePlugin:
    httpConn = None
    httpServerCon = None
    runAgain = 6

    lights = {}
   
    def __init__(self):
        return

    def HTTPRequest(self, Connection, URL):
        sendData = { 'Verb' : 'GET',
                'URL'  : URL,
                'Headers' : { 'Content-Type': 'text/xml; charset=utf-8', \
                            'Connection': 'keep-alive', \
                            'Accept': 'Content-Type: text/html; charset=UTF-8', \
                            'Host': Parameters["Address"]+":"+Parameters["Port"], \
                            'User-Agent':'Domoticz/1.0' }
            }
        Connection.Send(sendData)

    def registerDevices(self, ikeaDevices):
        i = 1
        if (len(Devices) == 0):
            i=1
        else:
            i=max(Devices)+1

        # whiteLevelNames, whiteLevelActions = colors.wbLevelDefinitions()
        # WhiteOptions = {"LevelActions": whiteLevelActions, "LevelNames": whiteLevelNames, "LevelOffHidden": "true","SelectorStyle": "0"}
        
        # colorLevelNames, colorLevelActions = colors.colorLevelDefinitions()
        # colorOptions = {"LevelActions": colorLevelActions, "LevelNames": colorLevelNames, "LevelOffHidden": "false", "SelectorStyle": "1"}

        ikeaIds = []
        # Add unregistred lights
        for aLight in ikeaDevices:
            Domoticz.Debug ("Registering: {0} - {1}".format(aLight['Id'], aLight['Name']))

            devID = str(aLight['Id'])
            ikeaIds.append(devID)

            if not "HasRGB" in aLight:
                aLight["HasRGB"] = False

            if not devID in self.lights:
                deviceType = 244
                subType = 73
                switchType = 7

                #if aLight['Dimmable']:
                #    switchType=7
                #else:
                #    switchType=0

                #Basic device
                Domoticz.Device(Name=aLight['Name'], Unit=i,  Type=deviceType, Subtype=subType, Switchtype=switchType, DeviceID=devID).Create()
                self.lights[devID] = {"DeviceID": aLight['Id'], "Unit": i}
                i=i+1

                #if aLight["HasRGB"]:
                #    Domoticz.Device(Name=aLight['Name'] + " - Color",  Unit=i, TypeName="Selector Switch", Switchtype=18, Options=colorOptions, DeviceID=devID+":CWS").Create()
                #    self.lights[devID+":CWS"] = {"DeviceID": devID+":CWS", "Unit": i}
                #    i=i+1
                                
                #if aLight['HasWB'] == True:
                #    Domoticz.Device(Name=aLight['Name'] + " - WB",  Unit=i, TypeName="Selector Switch", Switchtype=18, Options=WhiteOptions, DeviceID=devID+":WB").Create()
                #    self.lights[devID+":WB"] = {"DeviceID": devID+":WB", "Unit": i}
                #    i=i+1

        #Remove registered lights no longer found on the gateway
        for aUnit in list(Devices.keys()):
            devID = str(Devices[aUnit].DeviceID)

            if devID[-3:] == ":WB":
                devID = devID[:-3]

            if devID[-4:] == ":CWS":
                devID = devID[:-4]

            if not devID in ikeaIds:
                Devices[aUnit].Delete()

    def updateDeviceState(self, deviceState):
        
        Domoticz.Debug(str(deviceState))

        devID = str(deviceState["Id"])
        targetUnit = self.lights[devID]['Unit']
        nVal = 0

        sValInt = int((deviceState["Dimmer"]/254)*100)
        if sValInt == 0:
            sValInt = 1

        sVal = str(sValInt)

        if deviceState["State"] == "On":
            nVal = 1
        if deviceState["State"] == "Off":
            nVal = 0

        Devices[targetUnit].Update(nValue=nVal, sValue=sVal)

        # if "Hex" in aDev:
        #     if aDev["Hex"] != None:
        #         if devID+":WB" in self.lights:
        #             wbdevID = devID+":WB"
        #             targetUnit = self.lights[wbdevID]['Unit']
        #             Devices[targetUnit].Update(nValue=nVal, sValue=str(colors.wbLevelForHex(aDev['Hex'])))

        #         if devID+":CWS" in self.lights:
        #             wbdevID = devID+":CWS"
        #             targetUnit = self.lights[wbdevID]['Unit']
        #             Devices[targetUnit].Update(nValue=nVal, sValue=str(colors.colorLevelForHex(aDev['Hex'])))


    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()

        if len(Devices) > 0:
            # Some devices are already defined 
            for aUnit in Devices:
                self.lights[Devices[aUnit].DeviceID] = {"DeviceID": Devices[aUnit].DeviceID, "Unit": aUnit}

        # Enable server-connection
        self.httpServerConn = Domoticz.Connection(Name="Server Connection", Transport="TCP/IP", Protocol="HTTP", Port="8087")
        self.httpServerConn.Listen()

        # Enable client-connection
        self.httpConn = Domoticz.Connection(Name="HTTP Test", Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port=Parameters["Port"])
        self.httpConn.Connect()

    def onStop(self):
        Domoticz.Log("onStop - Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Debug("Tradfri connected successfully.")
            self.HTTPRequest(Connection, "/lights")
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["Address"]+":"+Parameters["Port"]+" with error: "+Description)

    def onMessage(self, Connection, Data):
        if Parameters["Mode6"] == "Debug":
            DumpHTTPResponseToLog(Data)
        
        strData = Data["Data"].decode("utf-8", "ignore")
        Status = int(Data["Status"])
    
        if (Status == 200):
            # Domoticz.Log(strData)
            command = json.loads(strData)
        
            if command['status'] == "Ok":
                action = command['action']
                # Domoticz.Log(action)

                if action == "getLights":
                    self.registerDevices(command['result'])

                elif action == "setState":
                    self.updateDeviceState(command['result'])

            else:
                Domoticz.Log(command['status'])

        elif (Status == 302):
            Domoticz.Log("Request returned a Page Moved Error.")
            sendData = { 'Verb' : 'GET',
                         'URL'  : Data["Headers"]["Location"],
                         'Headers' : { 'Content-Type': 'text/xml; charset=utf-8', \
                                       'Connection': 'keep-alive', \
                                       'Accept': 'Content-Type: text/html; charset=UTF-8', \
                                       'Host': Parameters["Address"]+":"+Parameters["Port"], \
                                       'User-Agent':'Domoticz/1.0' },
                        }
            Connection.Send(sendData)
        elif (Status == 400):
            Domoticz.Error("Request returned a Bad Request Error.")
        elif (Status == 500):
            Domoticz.Error("Request returned a Server Error.")
        else:
            Domoticz.Error("Request returned a status: "+str(Status))

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level)+", IkeaID: "+str(Devices[Unit].DeviceID))

        if (Devices[Unit].Type == 244) and (Devices[Unit].SubType == 73):
            if Command=="On":
                self.HTTPRequest(self.httpConn, "/lights/{0}/on".format(Devices[Unit].DeviceID))
            elif Command=="Off":
                self.HTTPRequest(self.httpConn, "/lights/{0}/off".format(Devices[Unit].DeviceID))
            elif Command=="Set Level":
                targetLevel = int(int(Level)*254/100)
                self.HTTPRequest(self.httpConn, "/lights/{0}/level/{1}".format(Devices[Unit].DeviceID, targetLevel))
               
    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called for connection to: "+Connection.Address+":"+Connection.Port)

    def onHeartbeat(self):
        if (self.httpConn.Connecting() or self.httpConn.Connected()):
            Domoticz.Debug("onHeartbeat called, Connection is alive.")
        else:
            self.runAgain = self.runAgain - 1
            if self.runAgain <= 0:
                self.httpConn.Connect()
                self.runAgain = 6
            else:
                Domoticz.Debug("onHeartbeat called, run again in "+str(self.runAgain)+" heartbeats.")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def LogMessage(Message):
    if Parameters["Mode6"] == "File":
        f = open(Parameters["HomeFolder"]+"http.html","w")
        f.write(Message)
        f.close()
        Domoticz.Log("File written")

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def DumpHTTPResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Log("HTTP Details ("+str(len(httpDict))+"):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Log("--->'"+x+" ("+str(len(httpDict[x]))+"):")
                for y in httpDict[x]:
                    Domoticz.Log("------->'" + y + "':'" + str(httpDict[x][y]) + "'")
            else:
                Domoticz.Log("--->'" + x + "':'" + str(httpDict[x]) + "'")
