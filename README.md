# Project 4.0 AI part

## Download requirements
1) `sudo apt update`
2) `sudo apt-get install pip swig python3-dev python3-setuptools`
2) Install wiringpi
    - `git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python.git`
    - `cd wiringOP-Python`
    - `python3 generate-bindings.py > bindings.i`
    - `sudo python3 setup.py install`
3) Install Docker
    - `curl -L get.docker.com | sh`
    - `sudo usermod -aG docker $USER`
    - `newgrp docker`
    - `docker run hello-world`
    - `docker stop hello-world`
4) Create the .env file
    - `echo -e "access_token=a\npayload=p" > .env`
5) `docker pull jorikgoris/project40-ai:testing-53cb65fc`
6) `docker run -it --rm --name project40-ai jorikgoris/project40-ai:IMAGE /bin/bash`
7) `sudo pip install -r requirements_hard.txt`
8) `sudo python3 relay.py`

## Application testing data
Videos used for testing tracking of the application:
- [Cars_Moving_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)
- [People_Walking_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)

## Development
- [cuda cores](https://pytorch.org/get-started/locally/) = `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`