import wiringpi, time, requests, sys

print("Start")
alarmLight = 4
alarmPower = 5
buttonPin = 0
wiringpi.wiringPiSetup()
wiringpi.pinMode(alarmLight, 1)
wiringpi.pinMode(alarmPower, 1)
wiringpi.pinMode(buttonPin, 0)

wiringpi.digitalWrite(alarmPower, 1)
on = True
try:
    #infinite loop - stop using Ctrl-C
    while True:
        if wiringpi.digitalRead(buttonPin) == 0:
            on = False
            time.sleep(5)
            
        if on: #reverse because relay activates if 2V or lower
            wiringpi.digitalWrite(alarmLight, 0)
        else:
            wiringpi.digitalWrite(alarmLight, 1)

        time.sleep(0.2) #anti bouncing

except KeyboardInterrupt:
    wiringpi.digitalWrite(alarmPower, 0)