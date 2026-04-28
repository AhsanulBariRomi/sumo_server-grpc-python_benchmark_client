#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <exception> // Added this

#include <grpcpp/grpcpp.h>
#include <libsumo/libsumo.h>
#include "vehicle.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class VehicleServiceImpl final : public VehicleService::Service {
  Status GetPosition(ServerContext* context, const PositionRequest* request, PositionResponse* reply) override {
      try {
          // Instantly grab the position
          libsumo::TraCIPosition pos = libsumo::Vehicle::getPosition(request->vehicle_id());
          reply->set_x(pos.x);
          reply->set_y(pos.y);
          return Status::OK;
      } catch (const std::exception& e) {
          // If the vehicle isn't on the road yet, send a clean error back to Python
          std::cerr << "SUMO Error: " << e.what() << std::endl;
          return Status(grpc::StatusCode::NOT_FOUND, e.what());
      } catch (...) {
          return Status(grpc::StatusCode::UNKNOWN, "Unknown C++ crash");
      }
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  VehicleServiceImpl service;
  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "gRPC Server listening on " << server_address << std::endl;
  server->Wait();
}

int main(int argc, char** argv) {
  std::cout << "Loading SUMO simulation..." << std::endl;
  std::vector<std::string> sumoArgs = {
    "-c", "helloworld.sumocfg",
    "--step-length", "0.001"
  };
  libsumo::Simulation::load(sumoArgs);
  //Step clock time check 
  std::cout << "SUCCESS: 1 Simulation Step = " << libsumo::Simulation::getDeltaT() << " seconds!" << std::endl;
  
  // CRITICAL FIX: Step the simulation forward 5 seconds so vehicles actually spawn!
  std::cout << "Stepping simulation forward to spawn vehicles..." << std::endl;
  for(int i = 0; i < 5; i++) {
      libsumo::Simulation::step();
  }
  
  RunServer();
  return 0;
}