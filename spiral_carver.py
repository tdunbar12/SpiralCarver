import tkinter as tk
from tkinter import ttk
import threading
import RPi.GPIO as GPIO
import sys

# Import Shared Data
from shared_spiral_carver import shared_data

# Motor Configuration
from motor import MotorDRV8825

# UI Utilities
from ui import (
    setup_ui,
    toggle_pause,
    quit_program
)

# Sequence Execution
from sequence import run_sequence, stop_motors

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Settings
motor1_pins = shared_data.get("motor1_pins")
motor2_pins = shared_data.get("motor2_pins")

motor1 = MotorDRV8825(motor1_pins["dir"], motor1_pins["step"], motor1_pins["enable"])
motor2 = MotorDRV8825(motor2_pins["dir"], motor2_pins["step"], motor2_pins["enable"])

# Add motors to shared_data
shared_data.set("motor1", motor1)
shared_data.set("motor2", motor2)

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


# UI Setup
root = tk.Tk()
root.title("Stepper Motor Control")
root.geometry("500x400")
root.protocol("WM_DELETE_WINDOW", lambda: quit_program(root))

# Initialize UI
setup_ui(
    root,
    lambda: run_sequence(),
    stop_motors,
    toggle_pause,
    lambda: quit_program(root)
)

# Run the application
root.mainloop()
