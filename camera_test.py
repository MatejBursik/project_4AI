import cv2

# Camera test

cap = cv2.VideoCapture(0)
 
if not cap.isOpened():
    print("Camera not accessible")
else:
    ret, frame = cap.read()
    if ret:
        print("Captured frame successfully")
    else:
        print("Failed to capture frame")
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGB)
        cv2.imshow("asd", frame)
        if cv2.waitKey(1) == ord('q'):
            break
 
cap.release()
cv2.destroyAllWindows