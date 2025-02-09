import requests, cv2, numpy as np

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

def draw_rect_with_label(x1, y1, x2, y2, frame, label, color = (0, 0, 255)):
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def draw_circle(x1, y1, x2, y2, frame, color = (0, 0, 255)):
    cv2.circle(frame, (int(x1+((x2-x1)/2)), int(y1+((y2-y1)/2))), 15, color, -1)
    return frame

def identify_color(image, find):
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    match find:
        # Define the range for color in HSV and create mask
        case "red":
            lower_1 = np.array([0, 50, 50])
            upper_1 = np.array([10, 255, 255])
            lower_2 = np.array([170, 50, 50])
            upper_2 = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv_image, lower_1, upper_1)
            mask2 = cv2.inRange(hsv_image, lower_2, upper_2)
            color_mask = cv2.bitwise_or(mask1, mask2)
        case "blue":
            lower = np.array([100, 60, 60])
            upper = np.array([120, 255, 255])
            color_mask = cv2.inRange(hsv_image, lower, upper)
        case "pink":
            # RGB pink = (180, 105, 255)
            lower = np.array([160, 100, 150])
            upper = np.array([175, 255, 255])
            color_mask = cv2.inRange(hsv_image, lower, upper)
    
    # Convert to RGB for visualization
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Calculate the average color value
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_pixels = cv2.bitwise_and(rgb_image, rgb_image, mask=color_mask)
    mean_rgb = cv2.mean(color_pixels, mask=color_mask)[:3] # Extract (R, G, B)
    
    return mean_rgb
