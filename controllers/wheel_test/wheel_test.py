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
        k, wheel, position, initial_time = turn(position,wheel,initial_time)
        
        matrix = create_matrix(range_image,threshold_distance)
        objects = detect_objects(matrix, threshold_distance)
        detection_output(robot,range_image)

        # print(len(range_image))
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)