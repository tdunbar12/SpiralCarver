import threading
from motor import MotorDRV8825

# Shared Data Store with Lock
class SharedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}

    def get(self, key):
        with self.lock:
            return self.data.get(key)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value

# Initialize Shared Data
shared_data = SharedData()

# Application-Specific Data
shared_data.set("latitude_ranges", [
    {"start": 45, "end": 35, "rotations": 10},
    {"start": 35, "end": 25, "rotations": 20},
    {"start": 25, "end": 15, "rotations": 40},
    {"start": 15, "end": 5, "rotations": 80},
    {"start": 5, "end": -5, "rotations": 160},
])

# Sphere Dimensions and Cutting Speed
shared_data.set("desired_cutting_speed", 0.5)  # mm/s
shared_data.set("sphere_radius", 5.0 / 2)  # Radius in mm

# Motor Steps and Gear Ratios
motor_steps_per_revolution = 200
latitude_microstepping = 4
longitude_microstepping = 4
latitude_gear_ratio = 64
longitude_gear_ratio = 2.0

shared_data.set("steps_per_degree_latitude", 
    motor_steps_per_revolution * latitude_microstepping * latitude_gear_ratio / 360
)
shared_data.set("steps_per_degree_longitude", 
    motor_steps_per_revolution * longitude_microstepping * longitude_gear_ratio / 360
)

# GPIO Pin Assignments
shared_data.set("motor1_pins", {"dir": 13, "step": 19, "enable": 12})
shared_data.set("motor2_pins", {"dir": 24, "step": 18, "enable": 4})
"""
# Create motor instances from shared GPIO pin configurations
motor1_pins = shared_data.get("motor1_pins")
motor2_pins = shared_data.get("motor2_pins")

shared_data.set("motor1", MotorDRV8825(motor1_pins["dir"], motor1_pins["step"], motor1_pins["enable"]))
shared_data.set("motor2", MotorDRV8825(motor2_pins["dir"], motor2_pins["step"], motor2_pins["enable"]))
"""
# Functions for Calculation Utilities (if needed dynamically in shared data)
def calculate_longitude_rpm(cutting_speed, latitude, sphere_radius):
    latitude_circumference = 2 * 3.14159 * sphere_radius * math.cos(math.radians(latitude))
    return (cutting_speed * 60) / latitude_circumference

def calculate_longitude_delay(rpm, steps_per_degree):
    steps_per_minute = rpm * 360 * steps_per_degree
    return 60 / steps_per_minute

def calculate_latitude_delay(rotation_time, rotations, start_lat, end_lat, steps_per_degree_latitude):
    total_time = rotation_time * rotations
    steps = int(round(steps_per_degree_latitude * abs(start_lat - end_lat)))
    return total_time / steps

shared_data.set("calculate_longitude_rpm", calculate_longitude_rpm)
shared_data.set("calculate_longitude_delay", calculate_longitude_delay)
shared_data.set("calculate_latitude_delay", calculate_latitude_delay)
