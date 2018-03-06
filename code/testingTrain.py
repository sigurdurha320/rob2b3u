import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
enable = 18
HinputC = 23
HinputCC = 24
trnsC = 20
trnsCC = 21
responseC = 26
responseCC = 19

GPIO.setup(enable,GPIO.OUT)
GPIO.setup(HinputC,GPIO.OUT)
GPIO.setup(HinputCC,GPIO.OUT)
GPIO.setup(trnsC,GPIO.OUT)
GPIO.setup(trnsCC,GPIO.OUT)
GPIO.setup(responseC,GPIO.IN)
GPIO.setup(responseCC,GPIO.IN)

print("setting defaults")
GPIO.output(HinputC,0)
GPIO.output(HinputCC,0)
GPIO.output(trnsC,0)
GPIO.output(trnsCC,0)

print("Enableing H-bridge")

GPIO.output(enable,1)

def testRun():
        sleep(1)
        print("starting test")
        sleep(1)
	Counter = 0
	runs = 6
	for i in range(runs):
                GPIO.output(HinputC,(i+1)%2)
                GPIO.output(trnsC,(i+1)%2)
                GPIO.output(HinputCC,i%2)   
                GPIO.output(trnsCC,i%2)
                sleep(0.8)
                if i%2==1:
                        print("Current flowing currectly: %s" % (GPIO.input(responseCC)))
                        if GPIO.input(responseCC)==1:
                                Counter+=1
                else:
                        print("Current flowing currectly: %s" % (GPIO.input(responseC)))
                        if GPIO.input(responseC)==1:
                                Counter+=1 
                sleep(0.2)
        GPIO.output(HinputC,0)
        GPIO.output(trnsC,0)
        GPIO.output(HinputCC,0)   
        GPIO.output(trnsCC,0)
        print("I got %s/%s possible responses" % (Counter,runs))	
        print("Turning Rocket off")
        if Counter==6:
                return True
        else:
                return False

def main():
        return

if testRun():
        main()
GPIO.cleanup()
