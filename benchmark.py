import contextlib
import os
import time
import traci
import grpc
import vehicle_pb2
import vehicle_pb2_grpc
# FIX 1: Tell SUMO exactly where its home folder is to kill the C++ Warning
os.environ["SUMO_HOME"] = "/home/mdahsanulbari/sumo"
VEHICLE_ID = "t_0" # Change this to whatever vehicle ID is in your rou.xml
ITERATIONS = 1000

def test_traci():
    # FIX 2: Temporarily mute Python's sys.stdout to kill the "Retrying" message
    with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
        
    # Connect standard TraCI to a running sumo.exe
        traci.start(["/home/mdahsanulbari/sumo/bin/sumo", 
                 "-c", "helloworld.sumocfg",
                 "--no-step-log", "true",
                 "--step-length", "0.001"])
        for _ in range(5):
            traci.simulationStep()

    pos = traci.vehicle.getPosition(VEHICLE_ID)
    print(f"  -> TraCI sees vehicle '{VEHICLE_ID}' at: X={pos[0]:.2f}, Y={pos[1]:.2f}")

    start_time = time.time()
    for _ in range(ITERATIONS):
        pos = traci.vehicle.getPosition(VEHICLE_ID)
    end_time = time.time()
    traci.close()
    print(f"TraCI Time for {ITERATIONS} calls: {end_time - start_time:.4f} seconds")

def test_grpc():
    # Connect to our custom C++ wrapper
    channel = grpc.insecure_channel('localhost:50051')
    stub = vehicle_pb2_grpc.VehicleServiceStub(channel)
    request = vehicle_pb2.PositionRequest(vehicle_id=VEHICLE_ID)

    response = stub.GetPosition(request)
    print(f"  -> gRPC sees vehicle '{VEHICLE_ID}' at: X={response.x:.2f}, Y={response.y:.2f}")
    
    start_time = time.time()
    for _ in range(ITERATIONS):
        response = stub.GetPosition(request)
    end_time = time.time()
    print(f"gRPC Time for {ITERATIONS} calls: {end_time - start_time:.4f} seconds")

if __name__ == '__main__':
    print("Testing gRPC...")
    test_grpc()
    print("Testing TraCI...")
    test_traci()
    # Note: To run the TraCI test, you would need sumo-launchd.py running in the background separately!