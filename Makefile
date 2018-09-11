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

$(tradfri): $(tradfri-src) $(dep)
	cd src/tradfri; $(dep) ensure -v; go install -v

$(tradfri-server): $(tradfri-server-src) $(dep)
	cd src/tradfri-server; $(dep) ensure -v; go install -v
	cd src/tradfri-server; cp -r styles $(GOPATH)/bin/; cp -r templates $(GOPATH)/bin/ 

$(tradfri-src): 
	git clone https://github.com/moroen/go-tradfri.git src/tradfri

$(tradfri-server-src):
	git clone https://github.com/moroen/go-tradfri-server.git src/tradfri-server

clean: 
	rm -f bin/tradfri
	rm -f bin/tradfri-server
	rm -rf src/tradfri/*
	rm -rf src/tradfri-server/*
	rm -rf src/github.com

$(dep):
	 go get -u github.com/golang/dep/cmd/dep

