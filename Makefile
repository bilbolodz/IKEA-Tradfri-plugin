export GOPATH=$(shell pwd)
dep = ${GOPATH}/bin/dep
python-libs = `pkg-config --cflags --libs python3`
srcdir = src/
src = $(srcdir)/coap.c $(srcdir)/coap.go

tradfri = bin/tradfri
tradfri-src = src/tradfri/*

canopus = src/github.com/moroen/canopus/*
go-tradfricoap = src/github.com/moroen/go-tradfricoap/*

# tradfri-own-deps = $(canopus) $(go-tradfricoap)

tradfri-server = bin/tradfri-server
tradfri-server-src = src/tradfri-server/*

all: $(tradfri) $(tradfri-server) 

$(tradfri): $(tradfri-src) $(tradfri-own-deps)
	cd src/tradfri; dep ensure -v; go install -v

$(tradfri-server): $(tradfri-server-src) $(tradfri-own-deps)
	cd src/tradfri-server; dep ensure -v; go install -v
	cd src/tradfri-server; cp -r styles $(GOPATH)/bin/; cp -r templates $(GOPATH)/bin/ 

$(tradfri-src) $(tradfri-server-src):
	git submodule init; git submodule update -f --remote

$(canopus):
	go get -v github.com/moroen/canopus

$(go-tradfricoap):
	go get -v github.com/moroen/go-tradfricoap
	


clean: 
	rm -f bin/tradfri
	rm -f bin/tradfri-server
	rm -rf src/tradfri/*
	rm -rf src/tradfri-server/*
	rm -rf src/github.com

$(dep):
	 go get -u github.com/golang/dep/cmd/dep

