import numpy as np
import time
from demands import *

def create_matrix(range_data, threshold_distance):
    rows = 16
    cols = resolution
    matrix = np.reshape(range_data, (rows,cols))
    '''
    # Initialize an empty matrix with the specified number of rows and columns
    matrix = np.zeros((rows, cols))
    
    # Fill the matrix according to the specified pattern
    for i in range(len(range_data)):
        row = i % rows
        col = i // rows
        matrix[row, col] = range_data[i]

    # print(matrix)
    '''
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
                else:
                    if object_start is not None:
                        object_end = (row, col-1)
                        objects.append((object_start, object_end))
                        object_start = None
                        # objects, object_start = define_objects(objects,object_start,object_end)
            else:
                if object_start is not None:
                    object_end = (row, col - 1)
                    objects.append((object_start, object_end))
                    object_start = None
        # Handle case where the row ends with an object part
        if object_start is not None:
            object_end = (row, cols - 1)
            objects.append((object_start, object_end))
            object_start = None
            
    return objects

# print detected objects
def detection_output(robot, range_image, position, wheel, initial_time):
    matrix = create_matrix(range_image, threshold_distance)
    objects = detect_objects(matrix, threshold_distance)
    # print(matrix)

    if objects:
        print("Detected {} objects:".format(len(objects)))
        for obj in objects:
            start_idx, end_idx = obj
            print("Object from {} to {}".format(start_idx, end_idx))
            print(start_idx[1])
            '''if start_idx[1] < 300 :
                print("Object too close, not turning")
                wheel.setVelocity(0.0)
                wheel.setPosition(0.0)
                continue  # Skip turning and proceed to the next object'''
            wheel.setVelocity(wheel_target_velocity)
            wheel.setPosition(wheel_angle)
            # Call the turn function when an object is detected
            k, wheel, position, initial_time = turn(position, wheel, initial_time)
            if initial_time is None:
                # If the turn is complete, break out of the loop
                break       
    else:
        print("No objects detected.")
        initial_time = None  # Reset initial_time if no objects detected
    
    return initial_time if initial_time is not None else None


# for Rotational Motor
def turn(position,wheel,initial_time):
    k = position.getValue()
    if k < wheel_angle + 0.01 and k > wheel_angle - 0.01:
        if initial_time is None:  # Check if it's the first time entering the if condition
            initial_time = time.time() * 1000.0  # Record the initial time
    
        current_time = time.time() * 1000.0
        time_difference = current_time - initial_time
        
        if time_difference >= 10000:  # Check if 2 seconds have passed
            wheel.setPosition(0.0)
    print(k)
    return k, wheel, position, initial_time