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
    for row in range(rows - excluded_layers):
        for col in range(cols):
            distance = matrix[row, col]  # Retrieve the distance value
            if distance >= ignored_distance:  # Ignore distances smaller than 3
                if distance < threshold_distance:
                    if object_start is None:
                        object_start = (row, col)
                elif object_start is not None:
                    object_end = (row, col)
                    # Check for overlapping indices between current and previous objects
                    for i in range(len(objects)):
                        prev_start, prev_end = objects[i]
                        if any(cols in range(prev_start[0], prev_end[0]) for cols in range(object_start[0], object_end[0])):
                            # If there's overlap, merge objects
                            objects[i] = (min(prev_start[0], object_start[0]), min(prev_start[1], object_start[1])), (max(prev_end[0], object_end[0]), max(prev_end[1], object_end[1]))
                            object_start = None  # Reset object_start as it's merged with previous one
                            break
                        else:
                            # If no overlap with any previous object, delete previous object and append as new object
                            objects[:] = [obj for obj in objects if obj != (object_start, object_end)]
                            objects.append((object_start, object_end))
                            object_start = None
    if object_start is not None:
        objects.append((object_start, object_end))
        
    return objects




def merge_objects(range_data, threshold_distance):
    rows = 16
    cols = resolution
    
    # Reshape the data array into a matrix with the specified number of columns
    matrix = np.reshape(range_data, (rows,cols))
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
                # print("Object from {} to {}".format(start_idx, end_idx))
                print(objects)
        else:
            print("No objects detected.")
            # print(len(range_image))
        
        merge_objects(range_image, threshold_distance)
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)