from dronekit import connect

connection_string = '127.0.0.1:14550'

vehicle = connect(connection_string, wait_ready=True)

print("Autopilot firmware version: %s" % vehicle.version)
print("GPS: %s" % vehicle.gps_0)
print("Battery: %s" % vehicle.battery)
print("Last heartbeat: %s" % vehicle.last_heartbeat)
print("Armable?: %s" % vehicle.is_armable)
print("System status: %s" % vehicle.system_status.state)
print("Mode: %s" % vehicle.mode.name)

vehicle.close()
