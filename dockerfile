# Use an official Python 3.11.5 base image
# FROM python:3.11.5-slim
FROM --platform=linux/arm64 python:3.11.5-slim

# Update the image
RUN apt update && apt upgrade -y
RUN apt install libglib2.0-0 -y
RUN apt install libgl1 -y

# Set the working directory in the container
WORKDIR /app

# Copy all necessery files
COPY requirements_con.txt .
COPY YOLO_model/first_model.onnx YOLO_model/
COPY functions.py .
COPY main.py .
COPY test_data/cropped.mp4 test_data/
COPY .env .
COPY cronjob_access_token.py .

# Cron job
COPY crontab.txt /etc/cron.d/mycron
RUN chmod +x /app/cronjob_access_token.py
RUN chmod 0644 /etc/cron.d/mycron && crontab /etc/cron.d/mycron

# Install Python dependencies, including YOLOv5 Ultralytics
RUN pip install --upgrade pip
RUN pip install -r requirements_con.txt

EXPOSE 5500:5500

# Run the startup script
COPY con_bootup.sh con_bootup.sh
RUN chmod +x con_bootup.sh
CMD ["con_bootup.sh"]
