import numpy as np
import time
from controller import Robot # type: ignore

# Constants
threshold_distance = 15.0
ignored_distance = 3.0
resolution = 900
excluded_layers = 15
timestep = 32

def transform_data(range_data):
    transformed_data = []
    for data in range_data:
        transformed_data.append(int.from_bytes(data, byteorder='big', signed=True))
    return transformed_data

def Lidar_sensor(robot):
    lidar = robot.getDevice('lidar')
    lidar.enable(timestep)
    return lidar

# Create the Robot instance.
robot = Robot()

lidar = Lidar_sensor(robot)

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

def create_matrix(range_data, threshold_distance):
    rows = 16
    cols = resolution
    matrix = np.reshape(range_data, (rows, cols))
    # matrix = np.reshape(range_data, (cols, rows))
    # matrix = matrix.transpose()
    return matrix

def define_objects(objects, object_start, object_end):
    merged = False
    for i, (prev_start, prev_end) in enumerate(objects):
        if any(col in range(prev_start[1], prev_end[1]+1) for col in range(object_start[1], object_end[1]+1)):
            new_start = (min(prev_start[0], object_start[0]), min(prev_start[1], object_start[1]))
            new_end = (max(prev_end[0], object_end[0]), max(prev_end[1], object_end[1]))
            objects[i] = (new_start, new_end)
            merged = True
            break
    if not merged:
        objects.append((object_start, object_end))
    return objects

def detect_objects(matrix, threshold_distance):
    objects = []
    object_start = None
    rows, cols = matrix.shape
    
    for row in range(rows - excluded_layers):
        for col in range(cols):
            distance = matrix[row, col]
            if distance >= ignored_distance:
                if distance < threshold_distance:
                    if object_start is None:
                        object_start = (row, col)
                else:
                    if object_start is not None:
                        object_end = (row, col-1)
                        objects = define_objects(objects, object_start, object_end)
                        object_start = None
            else:
                if object_start is not None:
                    object_end = (row, col - 1)
                    objects = define_objects(objects, object_start, object_end)
                    object_start = None
        if object_start is not None:
            object_end = (row, cols - 1)
            objects = define_objects(objects, object_start, object_end)
            object_start = None
    return objects

def detection_output(robot, range_image, stop_everything):
    # in case we have bytes
    # transformed_data = transform_data(range_image)
    # matrix = create_matrix(transformed_data, threshold_distance)
    matrix = create_matrix(range_image, threshold_distance)
    objects = detect_objects(matrix, threshold_distance)

    if objects and not stop_everything:
        stop_everything = True
        print("Detected {} objects:".format(len(objects)))
        for obj in objects:
            start_idx, end_idx = obj
            print("Object from {} to {}".format(start_idx, end_idx))
    else:
        start_idx, end_idx = None, None

    return stop_everything

# Main loop:
stop_everything = False
while robot.step(timestep) != -1:
    # Read the distance sensor data
    range_image = lidar.getRangeImage()
    
    # Call the detection_output function
    stop_everything = detection_output(robot, range_image, stop_everything)
