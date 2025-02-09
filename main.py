from ultralytics import YOLO
import cv2, requests, time

# https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/

def run_request(run):
    url = "http://192.168.137.2:5500/updateRun"

    # Create the data payload
    data = {
        "run": run
    }

    # Send the POST request
    try:
        response = requests.post(url, json=data)

        # Check for successful response
        if response.status_code == 200:
            print("Response from API:", response.json())
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Test api communcation from the container to localhost
#run_request(True)
#time.sleep(5)
#run_request(False)

# Load the YOLOv11 model
model = YOLO("YOLO_model/first_model.onnx")

path = "app_test_data/full.mp4" # path for camera = 0, path for video = "app_test_data/video.mp4"
cap = cv2.VideoCapture(path)

# Save as video
frames = []

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Perform tracking on the current frame
    result = model.track(frame)

    # Display the results
    annotated_frame = result[0].orig_img
    if result[0].boxes.id != None:
        for i, id in enumerate(result[0].boxes.id):
            if float(result[0].boxes.conf[0]) > 0.1:
                x1, y1, x2, y2 = result[0].boxes.xyxy[i]
                label = f"{int(id)} {result[0].names[int(result[0].boxes.cls[i])]}: {float(result[0].boxes.conf[0]):.3f}"
                color = (0, 0, 255)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    else:
        print("no boxes")


    # Show the frame with the annotations
    cv2.imshow('YOLOv11 Tracking', annotated_frame) # comment out for deployment
    frames.append(annotated_frame)

    # Press 'q' to stop
    if cv2.waitKey(1) == ord('q'):
        break

# comment out for deployment
"""
height, width, layers = frames[0].shape
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' for MP4 output
video_writer = cv2.VideoWriter("output_video.mp4", fourcc, 30, (width, height))

for f in frames:
    video_writer.write(f)
    
# Release the VideoWriter
video_writer.release()
"""
cap.release()
cv2.destroyAllWindows()
