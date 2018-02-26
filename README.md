A Domoticz plugin for IKEA Trådfri (Tradfri) gateway

# Plugin
Since domoticz plugins doesn't support COAP and also doesn't allow threads or async calls, the IKEA-tradfri plugin contains two parts, the domoticz plugin and a ikea-tradfri http-server written in GO. The server needs to be running at all times, and is intented to be run as a service using systemd. A command-line utilty for managing tradfri devices is also included.

# Requirements
1. Domoticz compiled with support for python / latest beta
2. golang tool-chain
3. libssl

## Installing requirements on linux/raspberry pi
```shell
  $ sudo apt-get install golang libssl-dev
```
## Installing requirements on macOS (using homebrew)
```shell
  $ brew install openssl@1.1
  $ brew install golang
```

# Building the tradfri-server and commandline tool
```shell
  $ make
```

# Use commandline tool to create a new ident
```shell
  $ bin/tradfri gateway createid IP GATEWAY-KEY IDENT
```
where GATEWAY-KEY is the security-key located on the bottom of the gateway, IDENT is the desired identifikation-name, and IP the address of the gateway.

Note: This command MUST be run as the same user that later will be used to run the server, as the config is stored in the user directory. (on linux/osx: ~/.config/tradfri)

# Test communication with the gateway
```shell
  $ bin/tradfri list
```
If successfull, this should print a list of all connected devices

# Run server (for testing)
```shell
  $ bin/tradfri-server
```

# Run server from systemd
To be added...

# Usage
Lights and devices have to be added to the gateway as per IKEA's instructions, using the official IKEA-tradfri app. 
