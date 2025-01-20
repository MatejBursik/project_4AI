# Project 4.0 AI part

## Download requirements
1) `sudo apt update`
2) Install Docker
    - `sudo apt install -y apt-transport-https ca-certificates curl software-properties-common`
    - `curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
    - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian bullseye stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
    - `sudo apt install -y docker-ce docker-ce-cli containerd.io`
    - If you want to check your version: `docker --version`
    - `sudo usermod -aG docker $USER`
    - Test Docker: `docker run hello-world`
    - If it doesn't work try this trouble shoot:
        - `sudo usermod -aG docker $USER`
        - `newgrp docker`
        - `docker run hello-world`
        - `docker stop hello-world`
3) `docker pull jorikgoris/project40-ai:testing-2386b9e6`
4) `docker run -it -d --rm jorikgoris/project40-ai:testing-2386b9e6`
5) Install wiringpi
    - `git clone https://github.com/orangepi-xunlong/wiringOP`
    - `cd wiringOP`
    - `sudo ./build clean`
    - `sudo ./build`
6) `sudo python3 relay.py`

- `apt-get install python3-venv`
- `python3.11 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements_hard.txt`
- `python3.11 main.py`

## Application testing data
Videos used for testing tracking of the application:
- [Cars_Moving_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)
- [People_Walking_Stock_Footage.mp4](https://www.youtube.com/watch?v=Y1jTEyb3wiI)