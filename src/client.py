#  import RPI.GPIO as GPIO
import sys

def lights_off():
    print("Light off!")
    #  GPIO.output(13, GPIO.LOW)

def lights_on():
    print("Light on!")
    #  GPIO.output(13, GPIO.HIGH)

def main():
    #  GPIO.setwarnings(False)
    #  GPIO.setmode(GPIO.BOARD)
    #  GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
    
    if sys.argv[0]== "on":
        lights_on()
        return

    if sys.argv[0]== "off":
        lights_off()
        return

if __name__ == '__main__':
    main()


