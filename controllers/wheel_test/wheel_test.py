from controller import Robot # type: ignore
from demands import *
from devices import *
import time

def detect_objects(range_data, threshold_distance):
    # Detect objects based on threshold distance
    objects = []
    object_start = None
    for i, distance in enumerate(range_data):
        if distance < threshold_distance:
            if object_start is None:
                object_start = i
        elif object_start is not None:
            object_end = i - 1
            objects.append((object_start, object_end))
            object_start = None
    if object_start is not None:
        objects.append((object_start, len(range_data) - 1))
    return objects

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

        objects = detect_objects(range_image, threshold_distance)
        # Print detected objects
        if objects:
            print("Detected {} objects:".format(len(objects)))
            for obj in objects:
                start_idx, end_idx = obj
                print("Object from {} to {}".format(start_idx, end_idx))
        else:
            print("No objects detected.")
            
        # print("{}".format(range_image))

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)