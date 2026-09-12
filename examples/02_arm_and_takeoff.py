import time

from dronekit import VehicleMode, connect


def arm_and_takeoff(vehicle, target_altitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Changing to GUIDED mode")
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(1)
    print("Arming motors")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %s" % current_altitude)
        if current_altitude >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


vehicle = connect('127.0.0.1:14550', wait_ready=True)

arm_and_takeoff(vehicle, 20)

print("Landing")
vehicle.mode = VehicleMode("LAND")

vehicle.close()
