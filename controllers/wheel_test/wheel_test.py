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
    initial_time_turn = None
    stop_everything = False
    start = time.time() * 1000

    while robot.step(timestep) != -1:

        end = time.time() * 1000
        time_elapsed = end - start
        if time_elapsed >= 30000:
            propeller.setVelocity(0.0) 
            break

        if not stop_everything :
            range_image = lidar.getRangeImage()
        
        initial_time, initial_time_turn, stop_everything,propeller = detection_output(robot, range_image, position, wheel, initial_time, stop_everything, initial_time_turn,propeller)
        
        if initial_time is None:
            # Continue moving forward if not turning
            wheel.setVelocity(wheel_target_velocity)

        # print(len(range_image))
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)