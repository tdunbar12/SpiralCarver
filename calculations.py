import math
from shared_spiral_carver import shared_data

def calculate_longitudinal_rotation_time(rpm):
    """
    Calculate the time required for one full longitudinal rotation.
    :param rpm: Revolutions per minute of the motor
    :return: Time per revolution in seconds
    """
    return 60 / rpm

def calculate_latitude_delay(rotation_time, rotations, start_lat, end_lat):
    """
    Calculate the delay between latitude steps.
    :param rotation_time: Time for one full rotation (seconds)
    :param rotations: Number of longitudinal rotations for the latitude range
    :param start_lat: Starting latitude (degrees)
    :param end_lat: Ending latitude (degrees)
    :return: Delay per latitude step (seconds)
    """
    steps_per_degree_latitude = shared_data.get("steps_per_degree_latitude")
    total_time = rotation_time * rotations
    steps = int(round(steps_per_degree_latitude * abs(start_lat - end_lat)))
    return total_time / steps

def calculate_longitude_rpm(cutting_speed, latitude, sphere_radius):
    """
    Calculate the RPM of the longitude motor based on cutting speed and latitude.
    :param cutting_speed: Desired cutting speed (mm/s)
    :param latitude: Latitude of the cut (degrees)
    :param sphere_radius: Radius of the sphere (mm)
    :return: Required RPM of the longitude motor
    """
    latitude_circumference = 2 * math.pi * sphere_radius * math.cos(math.radians(latitude))
    return (cutting_speed * 60) / latitude_circumference

def calculate_longitude_delay(rpm):
    """
    Calculate the delay between longitude steps.
    :param rpm: Revolutions per minute of the longitude motor
    :return: Delay per longitude step (seconds)
    """
    steps_per_degree_longitude = shared_data.get("steps_per_degree_longitude")
    steps_per_minute = rpm * 360 * steps_per_degree_longitude
    return 60 / steps_per_minute
