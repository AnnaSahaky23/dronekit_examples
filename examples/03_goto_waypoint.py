import time

from dronekit import LocationGlobalRelative, VehicleMode, connect


def arm_and_takeoff(vehicle, target_altitude):
    while not vehicle.is_armable:
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(1)

    vehicle.simple_takeoff(target_altitude)
    while True:
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            break
        time.sleep(1)


vehicle = connect('127.0.0.1:14550', wait_ready=True)

arm_and_takeoff(vehicle, 10)

home = vehicle.location.global_relative_frame
target = LocationGlobalRelative(home.lat + 0.0005, home.lon + 0.0005, 10)

print("Heading to waypoint")
vehicle.simple_goto(target)

for _ in range(10):
    current = vehicle.location.global_relative_frame
    print("lat=%s lon=%s alt=%s" % (current.lat, current.lon, current.alt))
    time.sleep(2)

print("Returning to launch")
vehicle.mode = VehicleMode("RTL")

vehicle.close()
