from time import sleep
from drivers import LedLight

if __name__ == "__main__":

    led = LedLight(5)

    led.on()
    sleep(1)
    led.off()
