export GOPATH=$(shell pwd)
dep = ${GOPATH}/bin/dep
python-libs = `pkg-config --cflags --libs python3`
srcdir = src/
src = $(srcdir)/coap.c $(srcdir)/coap.go

tradfri = bin/tradfri
tradfri-src = src/tradfri/*

tradfri-server = bin/tradfri-server
tradfri-server-src = src/tradfri-server/*

all: $(tradfri) $(tradfri-server) 

$(tradfri): $(tradfri-src) 
	cd src/tradfri; go get -v; go install -v

$(tradfri-server): $(tradfri-server-src)
	cd src/tradfri-server; go get -v; go install -v

$(tradfri-src) $(tradfri-server-src):
	git submodule init; git submodule update -f --remote



clean: 
	rm -f bin/tradfri
	rm -f bin/tradfri-server
	rm -rf src/tradfri/*
	rm -rf src/tradfri-server/*

$(dep):
	 go get -u github.com/golang/dep/cmd/dep

