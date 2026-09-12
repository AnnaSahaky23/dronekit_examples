import time


from dronekit import connect


vehicle = connect("127.0.0.1:14550", wait_ready=True)


def location_callback(self, attr_name, value):
    print("Location changed: lat=%s lon=%s" % (value.lat, value.lon))


def battery_callback(self, attr_name, value):
    print("Battery changed: %s" % value)


def mode_callback(self, attr_name, value):
    print("Mode changed to: %s" % value.name)


vehicle.add_attribute_listener('location.global_frame', location_callback)
vehicle.add_attribute_listener('battery', battery_callback)
vehicle.add_attribute_listener('mode', mode_callback)

time.sleep(15)

vehicle.remove_attribute_listener('location.global_frame', location_callback)
vehicle.remove_attribute_listener('battery', battery_callback)
vehicle.remove_attribute_listener('mode', mode_callback)

vehicle.close()
