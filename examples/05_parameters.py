import dronekit_sitl

vehicle = connect("127.0.0.1:14550", wait_ready=True)

print("Total parameters: %d" % len(vehicle.parameters))
print("WPNAV_SPEED: %s" % vehicle.parameters.get('WPNAV_SPEED'))
print("THR_MIN: %s" % vehicle.parameters.get('THR_MIN'))

print("Setting WPNAV_SPEED to 600 cm/s")
vehicle.parameters['WPNAV_SPEED'] = 600


def wpnav_speed_callback(self, attr_name, value):
    print("PARAMETER CALLBACK: WPNAV_SPEED changed to %s" % value)


vehicle.parameters.add_attribute_listener('WPNAV_SPEED', wpnav_speed_callback)

vehicle.parameters['WPNAV_SPEED'] = 700

vehicle.close()
