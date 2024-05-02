from controller import Robot # type: ignore
import numpy as np

def run_robot(robot):

    timestep = 32 # int(robot.getBasicTimeStep())

    # Lidar
    lidar = robot.getDevice('lidar')
    lidar.enable(timestep)

    # Rotational Motor (Propeller)
    propeller = robot.getDevice('motor')
    propeller.setPosition(float('inf'))  # Set position to infinity for continuous rotation
    
    # Set initial velocity of propeller (adjust as needed)
    propeller_target_velocity = 10000.0
    propeller.setVelocity(propeller_target_velocity)

    while robot.step(timestep) != -1:

        range_image = lidar.getRangeImage()
        print("{}".format(range_image))


if __name__ == "__main__":

    my_robot = Robot() # giati my_robot
    run_robot(my_robot)

'''
from controller import Robot, Supervisor

def run_robot(robot):

    timestep = int(robot.getBasicTimeStep())

    # Lidar
    lidar = robot.getDevice('lidar')
    lidar.enable(timestep)

    # Rotational Motor (Propeller)
    propeller = robot.getDevice('motor')
    propeller.setPosition(float('inf'))  # Set position to infinity for continuous rotation
    propeller_target_velocity = 5.0  # Set initial velocity of propeller (adjust as needed)
    propeller.setVelocity(propeller_target_velocity)

    while robot.step(timestep) != -1:

        # Get bounding object node
        bounding_object_node = robot.getFromDef("BOUNDING_OBJECT")
        
        # Check for collision with bounding object
        collision = lidar.getRangeImage()[0] < 0.2  # Adjust threshold as needed

        if collision:
            # Perform collision avoidance behavior
            print("Collision detected! Avoiding obstacle.")
            # Implement your collision avoidance behavior here

        # Your other code logic here

if __name__ == "__main__":
    # Create a Supervisor instance
    supervisor = Supervisor()
    
    # Load the robot model
    my_robot = supervisor.getFromDef('MY_ROBOT')
    
    # Ensure the robot is positioned at the initial location
    my_robot.restartController()
    
    # Run the robot
    run_robot(my_robot)
'''