## This project implements a co-simulation benchmark comparing the latency of 1,000 sequential TraCI requests against 1,000 gRPC requests. The system utilizes a custom C++ server loading SUMO into RAM via `libsumo` and communicates with a Python client.

# Phase 1: System & Environment Setup (Ubuntu / WSL)

## 1. Install WSL and Update Packages

If you haven't already, ensure your Windows Subsystem for Linux is installed and up to date:

```
wsl --install
sudo apt update
```

## 2. Install C++ and gRPC Build Tools

Install the core compilers and Google Protocol Buffer libraries:

```
sudo apt install -y build-essential protobuf-compiler protobuf-compiler-grpc libgrpc++-dev libprotobuf-dev
```

## 3. Install Python Dependencies

Since the benchmark runs in Python, install the required packages (gRPC tools and TraCI):

```
sudo apt update
sudo apt install -y python3-pip
pip3 install grpcio grpcio-tools traci
```

## 4. Install SUMO and libsumo

Add the official SUMO repository and install the binaries and libsumo development headers:

```
sudo add-apt-repository ppa:sumo/stable -y
sudo apt update
sudo apt install -y sumo sumo-tools libsumo-dev
```

Download the Source Code

```
cd ~
git clone --recursive https://github.com/eclipse-sumo/sumo
cd sumo
sudo apt-get install -y $(cat build_config/build_req_deb.txt build_config/tools_req_deb.txt)
cmake -B build .
cmake --build build -j$(nproc)
```

# Phase 2: Compiling the C++ gRPC Server

## 1. Navigate to the Project Directory

Open your WSL terminal and navigate to your mounted Windows drive where the project files live:

```
cd "/mnt/f/4. Academic(MSc)/Thesis/Thesis_PoC"
```

## 2. Generate the C++ Protobuf Bindings

Use the Linux protoc compiler to read vehicle.proto and generate the C++ communication headers:

```
protoc --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) vehicle.proto
```

(If successful, this will silently generate vehicle.pb.h, vehicle.pb.cc, vehicle.grpc.pb.h, and vehicle.grpc.pb.cc).

## 3. Compile the Server

Run the Makefile to link your server.cpp, the generated Protobuf files, and libsumo:

```
make
```

# Phase 3: Preparing the Python Benchmark

## 1. Generate the Python Protobuf Bindings

Still in the project directory, use Python's gRPC tools to generate the Python translation files for your benchmark script:

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. vehicle.proto
```

# Phase 4: Running the Co-Simulation Benchmark

You will need two WSL terminal windows open in your Thesis_PoC folder for this step.

## Terminal 1 (Start the Server):

Launch your custom C++ server, which uses libsumo to load the simulation into RAM and opens the gRPC port.

```
./server
```

## Terminal 2 (Run the Benchmark):

Execute the Python script to fire 1,000 sequential TraCI requests followed by 1,000 gRPC requests and compare the latency.

```
python3 benchmark.py
```

# Summary of Files You Should Have in the Folder

Before running Phase 2, your folder only needs these core files:

server.cpp (The C++ logic)

benchmark.py (The Python test script)

vehicle.proto (The data structure blueprint)

Makefile (The compiler instructions)

helloworld.sumocfg / rou.xml / net.xml (The SUMO traffic scenario files)

# Author:
Md Ahsanul Bari

MSc in DSE, TU Dresden
