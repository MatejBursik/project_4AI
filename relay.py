import wiringpi, time, threading
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
run = True
hard = False

# To turn off/on the killing device by AI
@app.route("/updateRun", methods=['POST'])
def updateRun():
    global run
    try:
        run = request.get_json()['run']
    except:
        print(Exception)

# Thread to run the Flask app
def flask_thread():
    app.run(host="127.0.0.1", port=5500, debug=True)    

flask_t = threading.Thread(target=flask_thread, daemon=True)
flask_t.start()

try:
    while True:
        # Check button state
        if wiringpi.digitalRead(buttonPin) == 0:
            hard = not hard
            print("button")
            time.sleep(1) # Anti-bouncing delay

        # Control the alarm light
        if run and hard:
            wiringpi.digitalWrite(alarmLight, 1)
            print("ON")
        else:
            wiringpi.digitalWrite(alarmLight, 0)
            print("OFF")

        time.sleep(0.2)  # Anti-bouncing delay
except KeyboardInterrupt:
    wiringpi.digitalWrite(alarmPower, 1)
    print("End")
