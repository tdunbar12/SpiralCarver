import tkinter as tk
from tkinter import ttk
import threading
import RPi.GPIO as GPIO
import sys

# Import Shared Data
from shared_spiral_carver import shared_data

# Global Variables for UI State
paused = False
pause_condition = threading.Condition()


def setup_ui(
    root, motor1, motor2, run_sequence, stop_motors, toggle_pause, quit_program
):
    """
    Setup the user interface for the application.
    :param root: Tkinter root window
    :param motor1: Longitude motor instance
    :param motor2: Latitude motor instance
    :param run_sequence: Function to start the sequence
    :param stop_motors: Function to stop motors
    :param toggle_pause: Function to toggle pause state
    :param quit_program: Function to quit the program
    """
    # Page 1: Manual Positioning
    frame_manual = ttk.Frame(root)
    ttk.Label(frame_manual, text="Manual Positioning").pack(pady=10)
    ttk.Button(frame_manual, text="Move Latitude Forward", command=lambda: motor2.turn_step("forward", 200, 0.002, lambda: True)).pack(pady=5)
    ttk.Button(frame_manual, text="Move Latitude Backward", command=lambda: motor2.turn_step("backward", 200, 0.002, lambda: True)).pack(pady=5)
    ttk.Button(frame_manual, text="Jog Latitude Forward", command=lambda: motor2.turn_step("forward", 1, 0.002, lambda: True)).pack(pady=5)
    ttk.Button(frame_manual, text="Jog Latitude Backward", command=lambda: motor2.turn_step("backward", 1, 0.002, lambda: True)).pack(pady=5)
    ttk.Button(frame_manual, text="Move to Start Latitude", command=lambda: motor2.turn_step("backward", 45, 0.002, lambda: True)).pack(pady=5)
    ttk.Button(frame_manual, text="Go to Run Page", command=lambda: show_page2(frame_manual, frame_run)).pack(pady=10)

    # Page 2: Run Program
    frame_run = ttk.Frame(root)
    ttk.Label(frame_run, text="Automated Program").pack(pady=10)
    ttk.Button(
        frame_run,
        text="Run Sequence",
        command=lambda: run_sequence()  # no arguements needed
    ).pack(pady=5)


    pause_button = ttk.Button(frame_run, text="Pause", command=toggle_pause)
    pause_button.pack(pady=10)
    ttk.Button(frame_run, text="Stop Motors", command=stop_motors).pack(pady=5)
    ttk.Button(frame_run, text="Back to Positioning Page", command=lambda: show_page1(frame_manual, frame_run)).pack(pady=10)
    ttk.Button(frame_run, text="Quit Program", command=lambda: quit_program(root)).pack(pady=10)

    # Status Indicators
    indicator_frame = ttk.Frame(root)
    indicator_frame.pack(fill="x", pady=10)
    ttk.Label(indicator_frame, text="Longitude Motor:").pack(side="left", padx=10)
    longitude_indicator = tk.Label(indicator_frame, width=10, bg="red")
    longitude_indicator.pack(side="left")
    ttk.Label(indicator_frame, text="Latitude Motor:").pack(side="left", padx=10)
    latitude_indicator = tk.Label(indicator_frame, width=10, bg="red")
    latitude_indicator.pack(side="left")

    # Status Bar
    status_var = tk.StringVar()
    status_var.set("Ready")
    ttk.Label(root, textvariable=status_var, anchor="w").pack(fill="x", side="bottom")

    # Start on Page 1
    show_page1(frame_manual, frame_run)

def update_status(message):
    """
    Update the status bar message.
    :param message: Message to display in the status bar
    """
    status_var.set(message)

def set_indicator_status(motor, running):
    """
    Update the status indicator for a motor.
    :param motor: 'longitude' or 'latitude'
    :param running: True if the motor is running, False otherwise
    """
    color = "green" if running else "red"
    if motor == "longitude":
        longitude_indicator.config(bg=color)
    elif motor == "latitude":
        latitude_indicator.config(bg=color)

def toggle_pause():
    """
    Toggle the pause state of the program.
    """
    global paused
    with pause_condition:
        paused = not paused
        if not paused:
            pause_condition.notify_all()
    pause_button.config(text="Resume" if paused else "Pause")

def wait_if_paused():
    """
    Pause execution if the program is in a paused state.
    """
    with pause_condition:
        while paused:
            pause_condition.wait()

def quit_program(root):
    """
    Quit the program gracefully.
    :param root: Tkinter root window
    """
    GPIO.cleanup()
    root.destroy()
    sys.exit()

def show_page1(frame_manual, frame_run):
    """
    Show the manual positioning page.
    :param frame_manual: Manual positioning frame
    :param frame_run: Run program frame
    """
    frame_run.pack_forget()
    frame_manual.pack()

def show_page2(frame_manual, frame_run):
    """
    Show the run program page.
    :param frame_manual: Manual positioning frame
    :param frame_run: Run program frame
    """
    frame_manual.pack_forget()
    frame_run.pack()
