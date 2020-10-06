#! /usr/bin/python
#Importer les libraries
import RPi.GPIO as GPIO
import time
import requests

# Set le mode des GPIO
GPIO.setmode(GPIO.BCM)

# Enleve les avertissements des GPIO
GPIO.setwarnings(False)

# Set les pins
pinpir = 17

# Set les pins en input
GPIO.setup(pinpir, GPIO.IN)


currentstate = 0
previousstate = 0

try:
    print("Waiting for PIR to settle ...")

    # Loop until PIR output is 0
    while GPIO.input(pinpir) == 1:

        currentstate = 0

    print(" Ready")

    # Loop jusqu'a ce que le programme arrete
    while True:

        # Read PIR state
        currentstate = GPIO.input(pinpir)

        # If the PIR is true
        if currentstate == 1 and previousstate == 0:

            print("Motion detected!")

            # Make POST request to IFTTT trigger
            r = requests.post('https://maker.ifttt.com/trigger/intruder_detected/with/key/EES-08VDUFYQYr-OsevEv', params={"value1":"none","value2":"none","value3":"none"})

            
            previousstate = 1

            #Wait 120 seconds before looping again
            print("Waiting 120 seconds")
            time.sleep(120)

        # Si PIR revient pret
        elif currentstate == 0 and previousstate == 1:

            print("Ready")
            previousstate = 0

        
        time.sleep(0.01)

except KeyboardInterrupt:
    print(" Quit")

    # Reset GPIO
    GPIO.cleanup()
