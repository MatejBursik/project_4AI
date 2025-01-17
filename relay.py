import wiringpi, time, sys
from flask import Flask, request

app = Flask(__name__)

alarmLight = 4
alarmPower = 5
buttonPin = 0
wiringpi.wiringPiSetup()
wiringpi.pinMode(alarmLight, 1)
wiringpi.pinMode(alarmPower, 1)
wiringpi.pinMode(buttonPin, 0)
wiringpi.digitalWrite(alarmPower, 0)
run = False
hard = True

# To turn off/on the killing device by AI
@app.route("/updateRun", methods=['POST'])
def updateRun():
    global run
    try:
        run = request.get_json()['run']
    except:
        print(Exception)

# To turn disable/enable the killing device manually
@app.route("/updateHard", methods=['POST'])
def updateRun():
    global hard
    try:
        hard = request.get_json()['hard']
    except:
        print(Exception)

app.run(host="127.0.0.1", port="5500", debug=True)

try:
    #infinite loop - stop using Ctrl-C
    while True:
        if wiringpi.digitalRead(buttonPin) == 0:
            hard = not hard
            print('button')
            time.sleep(1)
            
        if run and hard:
            wiringpi.digitalWrite(alarmLight, 1)
            print('on')
        else:
            wiringpi.digitalWrite(alarmLight, 0)
            print('off')

        time.sleep(0.2) #anti bouncing

except KeyboardInterrupt:
    wiringpi.digitalWrite(alarmPower, 1)
