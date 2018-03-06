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

def stop():
    GPIO.output(HinputC,0)
    GPIO.output(HinputCC,0)
    GPIO.output(trnsC,0)
    GPIO.output(trnsCC,0)


def PolarRun(reverse):
    GPIO.output(HinputC,(reverse+1)%2)
    GPIO.output(trnsC,(reverse+1)%2)
    GPIO.output(HinputCC,reverse)   
    GPIO.output(trnsCC,reverse)

def listener(reverse):
    if reverse:
        if GPIO.input(responseCC)==1:
            return True
    else:
        if GPIO.input(responseC)==1:
            return True
    return False

print("setting defaults")
stop()

print("Enableing H-bridge")

GPIO.output(enable,1)

def testRun(runs):
    sleep(1)
    print("starting test")
    sleep(1)
    Counter = 0
    for i in range(runs):
        PolarRun(i%2)
        sleep(0.8)
        response = listener(i%2)
        print("Current flowing currectly: %s" % (response))
        if response:
            Counter+=1
        sleep(0.2)
    stop()
    print("I got %s/%s possible responses" % (Counter,runs))	
    print("Turning Rocket off")
    if Counter==runs:
        return True
    else:
        return False

def main():
    PolarRun(0)
    while listener(0):
          pass
    stop()
    if testRun(6):
        main()

if testRun(6):
    main()
GPIO.cleanup()
