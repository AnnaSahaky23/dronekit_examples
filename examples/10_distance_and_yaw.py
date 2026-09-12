import math
import time

from pymavlink import mavutil

from dronekit import LocationGlobalRelative, VehicleMode, connect


def get_distance_metres(location1, location2):
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def condition_yaw(vehicle, heading, relative=False):
    is_relative = 1 if relative else 0
    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        heading,
        0,
        1,
        is_relative,
        0, 0, 0)
    vehicle.send_mavlink(msg)


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



vehicle = connect("127.0.0.1:14550", wait_ready=True)

arm_and_takeoff(vehicle, 10)

home = vehicle.location.global_relative_frame
target = LocationGlobalRelative(home.lat + 0.0006, home.lon, 10)
vehicle.simple_goto(target)

print("Pointing nose to 90 degrees (east)")
condition_yaw(vehicle, 90)

while True:
    current = vehicle.location.global_relative_frame
    distance = get_distance_metres(current, target)
    print("Distance to target: %.1f m, heading: %s" % (distance, vehicle.heading))
    if distance < 1:
        print("Reached target")
        break
    time.sleep(2)

vehicle.mode = VehicleMode("RTL")

vehicle.close()
