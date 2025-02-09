from ultralytics import YOLO
import cv2

from functions import *

# https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/

# Test api communcation from the container to localhost
#run_request(True)
#time.sleep(5)
#run_request(False)

# Load the YOLOv11 model
model = YOLO("YOLO_model/first_model.onnx")

path = "test_data/cropped.mp4" # path for camera = 0, path for video = "test_data/video.mp4"
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
            if float(result[0].boxes.conf[0]) > 0.5:
                x1, y1, x2, y2 = result[0].boxes.xyxy[i]
                # Drawing funcitons
                #frame = draw_circle(x1, y1, x2, y2, frame, (180, 105, 255))
                #label = f"{int(id)} {result[0].names[int(result[0].boxes.cls[i])]}: {float(result[0].boxes.conf[0]):.3f}"
                #frame = draw_rect_with_label(x1, y1, x2, y2, frame, label)
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
fourcc = cv2.VideoWriter_fourcc(*"mp4v") # Use 'mp4v' for MP4 output
video_writer = cv2.VideoWriter("color_test_3.mp4", fourcc, 30, (width, height))

for f in frames:
    video_writer.write(f)
    
# Release the VideoWriter
video_writer.release()
"""
cap.release()
cv2.destroyAllWindows()
