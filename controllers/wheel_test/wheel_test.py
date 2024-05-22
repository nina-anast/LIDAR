from controller import Robot # type: ignore
import numpy as np
from demands import *
from devices import *
from helpers import *
import time

def run_robot(robot):

    # Initialize Devices
    lidar = Lidar_sensor(robot)
    propeller = Propeller(robot)
    wheel = Wheel(robot)
    position = Position(robot)

    # Initialize angle and time
    k = 0
    initial_time = None  # Initialize initial_time variable outside the loop

    while robot.step(timestep) != -1:
        range_image = lidar.getRangeImage()
        
        initial_time = detection_output(robot, range_image, position, wheel, initial_time)
        
        if initial_time is None:
            # Continue moving forward if not turning
            wheel.setVelocity(wheel_target_velocity)

        # print(len(range_image))
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)