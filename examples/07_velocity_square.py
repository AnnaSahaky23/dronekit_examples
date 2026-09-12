import math
import time


from dronekit import VehicleMode, connect


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


def to_quaternion(roll=0.0, pitch=0.0, yaw=0.0):
    r = math.radians(roll * 0.5)
    p = math.radians(pitch * 0.5)
    y = math.radians(yaw * 0.5)

    cr, sr = math.cos(r), math.sin(r)
    cp, sp = math.cos(p), math.sin(p)
    cy, sy = math.cos(y), math.sin(y)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return [w, x, y, z]


def send_attitude_target(vehicle, roll_angle, pitch_angle, yaw_rate, thrust, duration):
    msg = vehicle.message_factory.set_attitude_target_encode(
        0,
        1, 1,
        0b00000000,
        to_quaternion(roll_angle, pitch_angle),
        0, 0, math.radians(yaw_rate),
        thrust)

    steps = int(duration / 0.1)
    for _ in range(steps):
        vehicle.send_mavlink(msg)
        time.sleep(0.1)


vehicle = connect("127.0.0.1:14550", wait_ready=True)

arm_and_takeoff(vehicle, 10)

print("Switching to GUIDED_NOGPS")
vehicle.mode = VehicleMode("GUIDED_NOGPS")
time.sleep(1)

hover_thrust = 0.5

print("Flying a square using attitude quaternions")
send_attitude_target(vehicle, 0, -10, 0, hover_thrust, 10)   # nose down, pitch forward
send_attitude_target(vehicle, 10, 0, 0, hover_thrust, 10)    # roll right
send_attitude_target(vehicle, 0, 10, 0, hover_thrust, 10)    # nose up, pitch back
send_attitude_target(vehicle, -10, 0, 0, hover_thrust, 10)   # roll left
send_attitude_target(vehicle, 0, 0, 0, hover_thrust, 2)     # level off

print("Landing")
vehicle.mode = VehicleMode("LAND")

vehicle.close()
