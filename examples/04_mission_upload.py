import time

from dronekit import Command, LocationGlobalRelative, VehicleMode, connect
from pymavlink import mavutil


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

home = vehicle.location.global_relative_frame
cmds = vehicle.commands
cmds.clear()

waypoints = [
    (home.lat + 0.0003, home.lon + 0.0000, 15),
    (home.lat + 0.0003, home.lon + 0.0003, 15),
    (home.lat + 0.0000, home.lon + 0.0003, 15),
]

cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                  0, 0, 0, 0, 0, 0, 0, 0, 15))

for lat, lon, alt in waypoints:
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0, 0, 0, 0, 0, 0, lat, lon, alt))

cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                  0, 0, 0, 0, 0, 0, 0, 0, 0))

cmds.upload()
print("Mission uploaded with %d waypoints" % len(waypoints))

arm_and_takeoff(vehicle, 15)

vehicle.commands.next = 0
vehicle.mode = VehicleMode("AUTO")

while True:
    next_wp = vehicle.commands.next
    print("Heading to waypoint %d" % next_wp)
    if next_wp >= len(waypoints) + 1:
        print("Mission complete")
        break
    time.sleep(2)

vehicle.close()
