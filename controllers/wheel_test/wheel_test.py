from controller import Robot # type: ignore
import numpy as np
from demands import *
from devices import *
import time

def detect_objects(matrix, threshold_distance):
    objects = []
    object_start = None
    rows, cols = matrix.shape
    
    # Iterate over rows and columns of the matrix
    for col in range(cols - excluded_layers):
        for row in range(rows):
            distance = matrix[row, col]  # Retrieve the distance value
            if distance < threshold_distance:
                if object_start is None:
                    object_start = (row, col)
            elif object_start is not None:
                object_end = (row, col - 1)
                # Check if the new object has the same row as the previous one
                if len(objects) > 0 and objects[-1][0][0] == object_start[0]:
                    # Merge objects by updating the end coordinate of the previous object
                    objects[-1] = (objects[-1][0], object_end)
                else:
                    objects.append((object_start, object_end))
                object_start = None
    
    # If an object extends to the end of the matrix
    if object_start is not None:
        object_end = (rows - 1, cols - 1)
        if len(objects) > 0 and objects[-1][0][0] == object_start[0]:
            objects[-1] = (objects[-1][0], object_end)
        else:
            objects.append((object_start, object_end))
    
    return objects

def merge_objects(range_data, threshold_distance):
    rows = resolution
    cols = 16
    
    # Reshape the data array into a matrix with the specified number of columns
    matrix = np.reshape(range_data, (resolution, cols))
    # print(matrix)
    
    return matrix

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
        # k = position.getValue()
        '''
        if k < wheel_angle + 0.01 and k > wheel_angle - 0.01:
            if initial_time is None:  # Check if it's the first time entering the if condition
                initial_time = time.time() * 1000.0  # Record the initial time
        
            current_time = time.time() * 1000.0
            time_difference = current_time - initial_time
            
            if time_difference >= 10000:  # Check if 2 seconds have passed
                wheel.setPosition(0.0)
        '''
        # print(k)
        matrix = merge_objects(range_image,threshold_distance)
        objects = detect_objects(matrix, threshold_distance)

        # Print detected objects
        if objects:
            print("Detected {} objects:".format(len(objects)))
            for obj in objects:
                start_idx, end_idx = obj
                print("Object from {} to {}".format(start_idx, end_idx))
        else:
            print("No objects detected.")
            # print(len(range_image))
        
        merge_objects(range_image, threshold_distance)
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)