import time


from dronekit import connect


vehicle = connect("127.0.0.1:14550", wait_ready=True)

print("RC channels before override: %s" % vehicle.channels)

print("Overriding channel 3 (throttle) to 1300")
vehicle.channels.overrides['3'] = 1300
time.sleep(3)
print("Channel 3 reading: %s" % vehicle.channels['3'])

print("Overriding channel 1 (roll) to 1700")
vehicle.channels.overrides['1'] = 1700
time.sleep(3)
print("Channel 1 reading: %s" % vehicle.channels['1'])

print("Clearing overrides")
vehicle.channels.overrides = {}
time.sleep(1)

vehicle.close()
