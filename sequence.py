import threading
from shared_spiral_carver import shared_data

# Global Flags
running = False
sequence_complete = False

# Sequence Execution Functions
def run_sequence():
    """
    Execute the carving sequence by controlling latitude and longitude motors.
    """
    global running, sequence_complete
    running = True
    sequence_complete = False

    def is_running():
        return running

    # Retrieve motors and parameters from shared data
    motor1 = shared_data.get("motor1")
    motor2 = shared_data.get("motor2")
    latitude_ranges = shared_data.get("latitude_ranges")
    desired_cutting_speed = shared_data.get("desired_cutting_speed")
    sphere_radius = shared_data.get("sphere_radius")
    steps_per_degree_latitude = shared_data.get("steps_per_degree_latitude")
    steps_per_degree_longitude = shared_data.get("steps_per_degree_longitude")

    calculate_longitude_rpm = shared_data.get("calculate_longitude_rpm")
    calculate_longitude_delay = shared_data.get("calculate_longitude_delay")
    calculate_latitude_delay = shared_data.get("calculate_latitude_delay")

    for range_data in latitude_ranges:
        if not is_running():
            break

        start_lat = range_data["start"]
        end_lat = range_data["end"]
        rotations = range_data["rotations"]

        # Calculate Parameters
        center_lat = (start_lat + end_lat) / 2
        longitude_rpm = calculate_longitude_rpm(desired_cutting_speed, center_lat, sphere_radius)
        longitude_delay = calculate_longitude_delay(longitude_rpm, steps_per_degree_longitude)
        rotation_time = 60 / longitude_rpm
        latitude_delay = calculate_latitude_delay(rotation_time, rotations, start_lat, end_lat, steps_per_degree_latitude)

        # Longitude Motor Thread
        threading.Thread(target=run_longitude, args=(longitude_delay,), daemon=True).start()

        # Latitude Motor Execution
        steps = int(round(steps_per_degree_latitude * abs(start_lat - end_lat)))
        for _ in range(steps):
            if not is_running():
                break
            motor2.turn_step("forward", 1, latitude_delay, is_running)

    sequence_complete = True

def run_longitude(delay):
    """
    Continuously run the longitude motor with the given delay.
    :param delay: Delay per step (seconds)
    """
    global running, sequence_complete
    motor1 = shared_data.get("motor1")
    while running and not sequence_complete:
        motor1.turn_step("forward", 1, delay, lambda: running)

def stop_motors():
    """
    Stop both motors and set the sequence flags to indicate completion.
    """
    global running, sequence_complete
    running = False
    sequence_complete = True
    motor1 = shared_data.get("motor1")
    motor2 = shared_data.get("motor2")
    motor1.stop()
    motor2.stop()

def toggle_pause():
    """
    Pause or resume the sequence.
    """
    global running
    running = not running

def quit_program():
    """
    Quit the program.
    """
    global running
    running = False
v