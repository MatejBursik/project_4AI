from ultralytics import YOLO
import cv2, time, os
from dotenv import load_dotenv

from functions import *

load_dotenv(".env")
token = os.getenv("access_token")
location_id = "asdfghjkl1"

# Load the YOLOv11 model
model = YOLO("YOLO_model/first_model.onnx")

path = "test_data/multi_color_test.mp4" # path for camera = 0, path for video = "test_data/video.mp4"
cap = cv2.VideoCapture(path)

# Save as video
frames = []

hornet_values = {
    "id": [],
    "coordinates": [],
    "enter_or_exit": [],
    "color": []
}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Perform tracking on the current frame
    # TODO: try while training so that it can be implemented for tracking
    # - obb model
    # - half (f16)
    # - imgsz
    # - look at more settings https://docs.ultralytics.com/modes/train/#train-settings
    result = model.track(frame, conf=0.6, max_det=3, iou=0.8)
    delete_ids = []

    # Display the results
    if result[0].boxes.id != None:
        for i, id in enumerate(result[0].boxes.id):
            if float(result[0].boxes.conf[0]) > 0.6:
                x1, y1, x2, y2 = result[0].boxes.xyxy[i]
                extracted_color, clr_text = identify_color(frame[int(y1):int(y2), int(x1):int(x2)])

                # Create an ID and coordinates list for new ID
                if id not in hornet_values["id"]:
                    # add coords (.append() adds to the back of the list)
                    hornet_values["id"].append(int(id))
                    hornet_values["coordinates"].append([])
                    hornet_values["enter_or_exit"].append("enter")
                    hornet_values["color"].append([])

                # add coords (.append() adds to the back of the list)
                hornet_values["coordinates"][int(id)-1].append(midpoint(int(x1), int(y1), int(x2), int(y2)))
                hornet_values["color"][int(id)-1].append(clr_text)

                # Drawing funcitons (debug)
                #frame = draw_circle(x1, y1, x2, y2, frame, (180, 105, 255))
                label = f"{int(id)} {result[0].names[int(result[0].boxes.cls[i])]}: {float(result[0].boxes.conf[0]):.3f} {clr_text}"
                frame = draw_rect_with_label(x1, y1, x2, y2, frame, label, extracted_color)

        for h_id in hornet_values["id"]:
            # If the hornet is not detected, DELETE its oldest coordinates
            if h_id not in result[0].boxes.id:
                # delete coords (.pop(0) deletes to the front of the list)
                hornet_values["coordinates"][h_id-1].pop(0)
                hornet_values["color"][h_id-1].pop(0)
            
            print("id:", h_id, ", lenght:", len(hornet_values["coordinates"][h_id-1])) # debug
            print(hornet_values["coordinates"][h_id-1]) # debug
            match len(hornet_values["coordinates"][h_id-1]):
                # If there are no coordinates in the list, DELETE the list and the id
                case 0:
                    delete_ids.append(h_id)

                # If there are 3 coordinates, calculate the angle
                case 3:
                    screen_angle = enter_exit_calc(
                        hornet_values["coordinates"][h_id-1][2],
                        hornet_values["coordinates"][h_id-1][1],
                        hornet_values["coordinates"][h_id-1][0]
                    )
                    if screen_angle == -1:
                        print("Error")
                    else:
                        print(most_frequent_color(hornet_values["color"][h_id-1])) # debug
                        print(f"Angle relative to screen: {screen_angle:.2f} degrees") # debug
                        print(f"Is the hornnet exiting or entering: {hornet_values['enter_or_exit'][h_id-1]}") # debug
                        #app_send_data(token, location_id, most_frequent_color(hornet_values["color"][h_id-1]), hornet_values['enter_or_exit'][h_id-1], screen_angle)

                        # Switch enter for exit
                        if hornet_values["enter_or_exit"][h_id-1] == 'enter':
                            hornet_values["enter_or_exit"][h_id-1] = 'exit'
                        elif hornet_values["enter_or_exit"][h_id-1] == 'exit':
                            hornet_values["enter_or_exit"][h_id-1] = 'enter'
                
                # If there is more than 5 coordinates, DELETE its oldest coordinates
                case 6:
                    # delete coords (.pop(0) deletes to the front of the list)
                    hornet_values["coordinates"][h_id-1].pop(0)
                    hornet_values["color"][h_id-1].pop(0)
    else:
        print("no boxes")
        for h_id in hornet_values["id"]:
            hornet_values["coordinates"][h_id-1].pop(0)
            hornet_values["color"][h_id-1].pop(0)
            if len(hornet_values["coordinates"][h_id-1]) == 0:
                # If there are no coordinates in the list, DELETE the list and the id
                delete_ids.append(h_id)

    # DELETE everything related to ids marked for deletion
    for h_id in delete_ids[::-1]: # in reverse for that deleting does not effect other values
        hornet_values["coordinates"].pop(h_id-1)
        hornet_values["enter_or_exit"].pop(h_id-1)
        hornet_values["color"].pop(h_id-1)
    hornet_values["id"] = list(range(1, len(hornet_values["coordinates"]) + 1))

    # Show the frame with the annotations
    cv2.imshow('YOLOv11 Tracking', frame) # debug
    frames.append(frame) # debug
    time.sleep(0.2) # debug

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
