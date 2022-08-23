import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time

class LedLight:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


class Button:

    def __init__(self, input_pin):
        self.input_pin = input_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_down(self):
        return GPIO.input(self.input_pin) == GPIO.HIGH

    def add_event_listener(self, callback):

        def press_callback(channel):
            if callback.__code__.co_argcount > 0:
                callback(channel)
            else:
                callback()

        GPIO.add_event_detect(self.input_pin, GPIO.RISING, callback=press_callback)
