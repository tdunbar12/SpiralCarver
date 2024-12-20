import RPi.GPIO as GPIO
import time

class MotorDRV8825:
    def __init__(self, dir_pin, step_pin, enable_pin):
        """
        Initialize the motor driver with the given GPIO pins.
        :param dir_pin: GPIO pin for direction control
        :param step_pin: GPIO pin for step control
        :param enable_pin: GPIO pin for enabling/disabling the motor
        """
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

    def turn_step(self, direction, steps, step_delay, running_flag):
        """
        Rotate the motor by a specific number of steps in the given direction.
        :param direction: 'forward' or 'backward'
        :param steps: Number of steps to rotate
        :param step_delay: Delay between steps (seconds)
        :param running_flag: Function to check if the motor should continue running
        """
        GPIO.output(self.enable_pin, 1)  # Enable motor
        GPIO.output(self.dir_pin, GPIO.HIGH if direction == "forward" else GPIO.LOW)
        for _ in range(steps):
            if not running_flag():
                break
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(step_delay)
        GPIO.output(self.enable_pin, 0)  # Disable motor

    def stop(self):
        """
        Stop the motor by disabling it.
        """
        GPIO.output(self.enable_pin, 0)
