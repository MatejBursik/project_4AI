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

# Install Python dependencies, including YOLOv5 Ultralytics
RUN pip install --upgrade pip
RUN pip install -r requirements_con.txt

EXPOSE 5500:5500

# Set the command to run your YOLO script
CMD ["python", "main.py"]
