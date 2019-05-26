from time import sleep
import pigpio
from read_RPM import reader
import RPi.GPIO as GPIO
 
# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi() 

# Calibrate ESC
ESC_GPIO = 13
pi.set_servo_pulsewidth(ESC_GPIO, 1610) # Maximum throttle.
sleep(2)
pi.set_servo_pulsewidth(ESC_GPIO, 1000) # Minimum throttle.
sleep(2)

# Set up input pins for thumbwheel switch
BCD = [16,20,21]
for pin in BCD:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up RPM reader
RPM_GPIO = 14
SAMPLE_TIME = 2.0
tach = reader(pi, RPM_GPIO)

try:
    while 1:
        speed = 0
        # Loop through pins to return value of BCD counter
        for pin in BCD:
            # Left shift speed then OR by negated pin value
            speed = (speed << 1) | (1 ^ GPIO.input(pin))

        # Set ESC speed via PWM
        pi.set_servo_pulsewidth(ESC_GPIO, speed * 1000 / 7 + 1000)

        # Read RPM
        rpm = tach.RPM()

        sleep(SAMPLE_TIME)

finally:
    pi.set_servo_pulsewidth(ESC_GPIO, 0) # Stop servo pulses.
    pi.stop() # Disconnect pigpio.
