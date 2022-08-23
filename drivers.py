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


def cleanup_pins():
    GPIO.cleanup()


class StepperMotor:
    def __init__(self, stepper_pins: list):
        """
        :param stepper_pins: The four pins where the motor is connected. Like [7, 11, 13, 15]
        """

        self.stepper_pins = stepper_pins

        self.stepping_sequences = {
            "half": [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]
            ],

            "dual phase": [
                [1, 0, 0, 1],
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
            ]
        }

        GPIO.setmode(GPIO.BOARD)

    def move(self, rotation: int, time_between_steps: float = 0.002, step_type: str = "dual phase"):
        """
        :param rotation: Amount of steps to rotate. 512 steps is a full rotation (360º), 256 is half (180º), and so on.
        :param time_between_steps: Seconds between steps. Lower and the motor1 will go faster.
        :param step_type: Either "dual phase" or "half". Half is slightly stronger, dual is faster.
        :return:
        """

        # control_pins
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        if rotation > 0:
            # not reversed
            for i in range(int(rotation)):

                for stepStage in range(len(self.stepping_sequences[step_type])):

                    for pin in range(len(self.stepping_sequences[step_type][0])):
                        GPIO.output(self.stepper_pins[pin], self.stepping_sequences[step_type][stepStage][pin])
                    time.sleep(time_between_steps)

        elif rotation < 0:
            # Reversed
            for i in range(int(rotation) * -1):
                for stepStage in range(len(self.stepping_sequences[step_type][::-1])):
                    for pin in range(len(self.stepping_sequences[step_type][::-1][0])):
                        GPIO.output(self.stepper_pins[pin], self.stepping_sequences[step_type][::-1][stepStage][pin])
                    time.sleep(time_between_steps)


# untested
class Servo:
    def __init__(self, servo_controller_pin: int):
        """
        :param servo_controller_pin: The controller pin
        """

        self.servo_controller_pin = servo_controller_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_controller_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(servo_controller_pin, 50)
        self.pwm.start(0)

    def set_angle(self, angle, lifespan=0.5):
        """

        :param angle: Desired angle to move the servo.
        :param lifespan: Lifespan of servo move in seconds
        :return:
        """

        # set to desired angle
        duty = angle / 18 + 2
        GPIO.output(self.servo_controller_pin, True)
        self.pwm.ChangeDutyCycle(duty)

        # wait
        time.sleep(lifespan)

        # kill
        GPIO.output(self.servo_controller_pin, False)
        self.pwm.ChangeDutyCycle(0)
