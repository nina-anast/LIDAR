from controller import Robot # type: ignore
from demands import *

def Lidar_sensor(robot):

    lidar = robot.getDevice('lidar')
    lidar.enable(timestep)
    return lidar

def Propeller(robot):

    propeller = robot.getDevice('motor')
    propeller.setPosition(float('inf'))  # Set position to infinity for continuous rotation
    propeller.setVelocity(propeller_target_velocity)
    return propeller

def Wheel(robot):
    # Rotational Motor (wheel)
    wheel = robot.getDevice('wheel')
    wheel.setPosition(0.0)  # Set position to infinity for continuous rotation
    wheel.setVelocity(0.0)
    return wheel

def Position(robot):
    # PositionSensor (position)
    position = robot.getDevice("position")
    position.enable(timestep)
    return position