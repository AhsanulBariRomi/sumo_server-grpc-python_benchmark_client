CXX = g++
# Adding -pthread because Linux networking heavily uses threading
CXXFLAGS = -std=c++17 -Wall -pthread

# Point directly to the SUMO we just compiled in your Linux home folder
SUMO_DIR = $(HOME)/sumo
SUMO_INCLUDE = -I$(SUMO_DIR)/src

# The -Wl,-rpath flag is a Linux trick so the server knows exactly where to find the .so file when it runs
SUMO_LIB_DIR = -L$(SUMO_DIR)/bin -Wl,-rpath=$(SUMO_DIR)/bin

LIBS = -lgrpc++ -lgrpc -lprotobuf -lsumocpp

all: server

server: server.cpp vehicle.pb.cc vehicle.grpc.pb.cc
	$(CXX) $(CXXFLAGS) $(SUMO_INCLUDE) -o server server.cpp vehicle.pb.cc vehicle.grpc.pb.cc $(SUMO_LIB_DIR) $(LIBS)

clean:
	rm -f server
	