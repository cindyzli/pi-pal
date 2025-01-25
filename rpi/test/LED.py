import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 23


# Set LED pin as output

GPIO.setup(LED_PIN, GPIO.OUT)

# Create PWM object with frequency 50Hz

pwm = GPIO.PWM(LED_PIN, 50)



# Start PWM with initial duty cycle 50%

pwm.start(50)



# Adjust brightness (example: gradually increase brightness)

for i in range(0, 101, 10):

    pwm.ChangeDutyCycle(i)

    time.sleep(0.2)

for i in reversed(range(0, 101, 10)):

    pwm.ChangeDutyCycle(i)

    time.sleep(0.2)

# Clean up

pwm.stop()

GPIO.cleanup()