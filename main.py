from ultralytics import YOLO
import cv2

# https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/

# Load the YOLOv11 model
model = YOLO("YOLO_model\\yolo11n.pt")

path = 0 # path for camera = 0, path for video = "app_test_data\\People_Walking_Stock_Footage.mp4"
cap = cv2.VideoCapture(path)

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
            x1, y1, x2, y2 = result[0].boxes.xyxy[i]
            label = f"{int(id)} {result[0].names[int(result[0].boxes.cls[i])]}: {float(result[0].boxes.conf[0]):.3f}"
            color = (0, 0, 255)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    else:
        print("no boxes")


    # Show the frame with the annotations
    cv2.imshow('YOLOv11 Tracking', annotated_frame)

    # Press 'q' to stop
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()