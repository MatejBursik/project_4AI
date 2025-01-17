# Project 4.0 AI part

## Download requirements
1) Install Docker
2) `docker build -t hornet_detection:latest .`
3) `docker run -it -d --name hornet_detection:latest`
4) Install wiringpi
    - `git clone https://github.com/orangepi-xunlong/wiringOP`
    - `cd wiringOP`
    - `sudo ./build clean`
    - `sudo ./build`
5) `sudo python3 relay.py`

- `apt-get install python3-venv`
- `python3.11 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3.11 main.py`

## Application testing data
Videos used for testing tracking of the application:
- [Cars_Moving_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)
- [People_Walking_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)