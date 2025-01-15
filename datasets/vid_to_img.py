import cv2

def vid_to_img(path):
    cap = cv2.VideoCapture(path)
    count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Exit loop if no frame
        if not ret:
            break

        cv2.imwrite("images/frame_" + str(count) + ".png", frame)
        count += 1
        
    cap.release()

vid_to_img("full.mp4")
