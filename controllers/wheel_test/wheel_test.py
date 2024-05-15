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
    turning = False  # Track whether the robot is currently turning
    stop_turn_time = None  # Track when the robot stopped turning
    
    while robot.step(timestep) != -1:
        range_image = lidar.getRangeImage()
        # k, wheel, position, initial_time = turn(position,wheel,initial_time)
        
        matrix = create_matrix(range_image,threshold_distance)
        objects = detect_objects(matrix, threshold_distance)
        # detection_output(robot,range_image)

        if objects:
            k, wheel, position, initial_time, turning = turn_left(position, wheel, propeller, initial_time)
            if not turning:
                continue  # Exit the loop iteration immediately after stopping the turn
        else:
            if not turning:
                if stop_turn_time:
                    current_time = time.time() * 1000.0
                    if current_time - stop_turn_time < wait_duration:
                        # Wait for the specified duration
                        continue
                    else:
                        stop_turn_time = None  # Reset stop_turn_time after waiting
                wheel.setVelocity(wheel_target_velocity)  # Continue moving forward if not turning

        # print(len(range_image))
        # print("{}".format(range_image))
        print(k)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)