# Use an official Python 3.11.5 base image
# Since the wiring-pi library for Python runs on a 3.9 version and is needed to operate the GPIO pins,
# we decided to containerize the AI portion since it needs 3.11.5 and only needs the camera feed to operate.

# FROM python:3.11.5-slim
FROM --platform=linux/arm64 python:3.11.5-slim

# Update the image
RUN apt update && apt upgrade -y
RUN apt install libglib2.0-0 -y
RUN apt install libgl1 -y
RUN apt install cron -y

# Set the working directory in the container
WORKDIR /app

# Copy all necessery files for the AI operation
COPY requirements_con.txt .
COPY YOLO_model/first_model.onnx YOLO_model/
COPY functions.py .
COPY main.py .
COPY test_data/multi_color_test.mp4 test_data/
COPY .env .
COPY cronjob_access_token.py .

# Setup Cron job
COPY crontab.txt /etc/cron.d/mycron
RUN service cron start
RUN chmod +x /app/cronjob_access_token.py
RUN chmod 0644 /etc/cron.d/mycron && crontab /etc/cron.d/mycron

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements_con.txt

EXPOSE 5500:5500

# Run the startup script
COPY con_bootup.sh .
RUN chmod +x con_bootup.sh
CMD ["/app/con_bootup.sh"]
