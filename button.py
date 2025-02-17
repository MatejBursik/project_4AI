import os
import subprocess
import wiringpi
import time

# Pin configuratie (Orange Pi GPIO Mapping)
BUTTON_1 = 8  # Pin 15 op Orange Pi header
BUTTON_2 = 11  # Pin 19 op Orange Pi header

# Instellen van GPIO
wiringpi.wiringPiSetup()
wiringpi.pinMode(BUTTON_1, 0)  # Instellen als input
wiringpi.pinMode(BUTTON_2, 0)  # Instellen als input
wiringpi.pullUpDnControl(BUTTON_1, 2)  # Pull-up
wiringpi.pullUpDnControl(BUTTON_2, 2)  # Pull-up

# Docker en Git instellingen
GIT_REPO = "https://github.com/MatejBursik/project_4AI.git"
LOCAL_DIR = "/home/orangepi/project_4AI"
REQUIREMENTS_FILE = os.path.join(LOCAL_DIR, "requirements_hard.txt")


def clone_or_pull_repo():
    """
    Checks for updates in the code repository.
    """
    # Check if the repository needs to be pulled or cloned
    if os.path.exists(LOCAL_DIR):
        print("Updating existing code...")
        subprocess.run(["git", "-C", LOCAL_DIR, "pull"], check=True)
    else:
        print("Cloning GitLab repository...")
        subprocess.run(["git", "clone", GIT_REPO, LOCAL_DIR], check=True)
    print("Code is up-to-date.")

    print("Building docker container")
    subprocess.run(["docker", "build", "-t", "project40-ai:1.0e", "."], check=True)

def start_services():
    """
    Runs the AI docker container and start the relay script.
    Popen is async.
    """
    print("Running Docker container...")
    subprocess.Popen([
        "docker", "run", "-d", "--rm", "--device=/dev/video1", "--name", "project40-ai", "project40-ai:1.0"
    ])
    print("Docker container started.")

    print("Running relay.py...")
    subprocess.Popen([
        "sudo", "python3", os.path.join(os.getcwd(), "relay.py")
    ])
    print("relay.py started.")

def main():
    try:
        while True:
            if wiringpi.digitalRead(BUTTON_1) == 0:
                print("Button 1 PRESSED: cloning or updating github repo")
                clone_or_pull_repo()
                time.sleep(2)
            
            if wiringpi.digitalRead(BUTTON_2) == 0:
                print("Button 2 PRESSED: starting AI and API.")
                start_services()
                time.sleep(2)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Script ended.")

if __name__ == "__main__":
    main()
