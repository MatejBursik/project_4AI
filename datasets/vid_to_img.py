import cv2

def vid_to_img(path):
    cap = cv2.VideoCapture(path)
    count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Exit loop if no frame
        if not ret:
            print("exit",ret,frame)
            break
        
        cv2.imwrite("datasets/images/frame_" + str(count) + ".png", frame)
        count += 1
        print(count)
    
    cap.release()

vid_to_img("app_test_data/extra_full.mp4")
