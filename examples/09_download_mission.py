import time
from pymavlink import mavutil

from dronekit import Command, connect


vehicle = connect("127.0.0.1:14550", wait_ready=True)

home = vehicle.location.global_relative_frame
cmds = vehicle.commands
cmds.clear()

cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                  0, 0, 0, 0, 0, 0, home.lat + 0.0002, home.lon, 20))
cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                  0, 0, 0, 0, 0, 0, home.lat, home.lon + 0.0002, 20))
cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                  0, 0, 0, 0, 0, 0, home.lat, home.lon + 0.0022, 20))
cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                  0, 0, 0, 0, 0, 0, home.lat, home.lon + 0.0002, 20))
cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                  mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                  0, 0, 0, 0, 0, 0, home.lat, home.lon + 0.0022, 20))
cmds.upload()


cmds.download()
cmds.wait_ready()

print("Downloaded %d mission items" % cmds.count)
for i, cmd in enumerate(cmds):
    print("%d: lat=%s lon=%s alt=%s command=%s" %
          (i, cmd.x, cmd.y, cmd.z, cmd.command))

vehicle.close()
