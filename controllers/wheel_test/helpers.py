import numpy as np
import time
from demands import *

def create_matrix(range_data, threshold_distance):
    rows = 16
    cols = resolution
    
    # Reshape the data array into a matrix with the specified number of columns
    matrix = np.reshape(range_data, (rows,cols))
    # print(matrix)
    return matrix

def define_objects(objects,object_start,object_end):
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
    return objects, object_start

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
                    objects, object_start = define_objects(objects,object_start,object_end)
    if object_start is not None:
        objects.append((object_start, object_end))
    return objects

# print detected objects
def detection_output(robot, range_image):
    matrix = create_matrix(range_image,threshold_distance)
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

# for Rotational Motor
def turn_left(position, wheel, propeller, initial_time):
    k = position.getValue()
    if wheel_angle - 0.01 < k < wheel_angle + 0.01:
        if initial_time is None:
            initial_time = time.time() * 1000.0  # Record the initial time
    
        current_time = time.time() * 1000.0
        time_difference = current_time - initial_time
        
        if time_difference >= turn_duration:
            wheel.setPosition(0.0)
            wheel.setVelocity(0.0)
            propeller.setVelocity(propeller_target_velocity)
            print('Stopped turning')
            return k, wheel, position, None, False  # Stop turning and reset initial_time
        else:
            return k, wheel, position, initial_time, True  # Continue turning
    else:
        wheel.setPosition(wheel_angle)  # Start turning to the left
        wheel.setVelocity(wheel_target_velocity)
        propeller.setVelocity(0)
        return k, wheel, position, initial_time, True