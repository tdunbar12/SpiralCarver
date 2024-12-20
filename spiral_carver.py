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
