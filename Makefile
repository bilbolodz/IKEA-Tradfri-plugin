export GOPATH=$(shell pwd)
dep = ${GOPATH}/bin/dep
python-libs = `pkg-config --cflags --libs python3`
srcdir = src/
src = $(srcdir)/coap.c $(srcdir)/coap.go

tradfri = bin/tradfri
tradfri-server = bin/tradfri-server

$(tradfri): 
	cd src/tradfri; go get -v; go install -v

$(tradfri-server):
	cd src/tradfri-server; go get -v; go install -v

all: $(tradfri) $(tradfri-server) 

$(dep):
	 go get -u github.com/golang/dep/cmd/dep

