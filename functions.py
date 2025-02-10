import requests, cv2, numpy as np
from sklearn.linear_model import LinearRegression

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

def identify_color(image):
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    count = 0
    color = "black"
    for find in ["red", "blue", "pink"]:
        # Issues with blue mask:
        # it is too dark and starts picking up black
        # solutions:
        # - adjust saturation and value
        # - switch blue for another color since this is a inherite issue
        # with less vibrant colors
        match find:
            # Define the range for color in HSV and create mask
            case "red":
                lower_1 = np.array([0, 50, 50])
                upper_1 = np.array([10, 255, 255])
                lower_2 = np.array([170, 50, 50])
                upper_2 = np.array([180, 255, 255])
                mask1 = cv2.inRange(hsv_image, lower_1, upper_1)
                mask2 = cv2.inRange(hsv_image, lower_2, upper_2)
                new_mask = cv2.bitwise_or(mask1, mask2)
            case "blue":
                lower = np.array([100, 100, 130])
                upper = np.array([120, 255, 255])
                new_mask = cv2.inRange(hsv_image, lower, upper)
            case "pink":
                # RGB pink = (180, 105, 255)
                lower = np.array([160, 100, 150])
                upper = np.array([175, 255, 255])
                new_mask = cv2.inRange(hsv_image, lower, upper)

        new_count = cv2.countNonZero(new_mask)
        if new_count > count:
            color_mask = new_mask
            count = new_count
            color = find

    if 'color_mask' not in locals() or color_mask is None:
        color_mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)

    # Calculate the average color value
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_pixels = cv2.bitwise_and(rgb_image, rgb_image, mask=color_mask)
    mean_rgb = cv2.mean(color_pixels, mask=color_mask)[:3] # Extract RGB
    
    return mean_rgb, color

def enter_exit_calc(coord_1, coord_2, coord_3):
    X = np.array([coord_1[0], coord_2[0], coord_3[0]]).reshape(-1, 1)
    Y = np.array([coord_1[1], coord_2[1], coord_3[1]])

    # Train model
    model = LinearRegression()
    model.fit(X, Y)

    m = model.coef_[0] # Slope of the best-fit line
    screen_m = 0 # Horizontal slope of the screen
    print("m ",m)

    # Check for perpendicular lines
    if (m * screen_m) == -1:
        angle = 90.0
    else:
        # Compute the angle in radians
        angle_radians = np.arctan(abs((m - screen_m) / (1 + m * screen_m)))
        angle = np.degrees(angle_radians)

    # Return angle relative to the screen north
    if m < 0:
        return angle + 90
    elif m > 0:
        return abs(angle - 90)
    else:
        # If the fligh path is perfectly horizontal or vertical
        # the magnitude/slope is 0 and can not determine which it is
        # so it needs to be determined by the points. If all X values
        # are the same then it is perfectly vertical and if all Y values
        # are the same then it is perfectly horizontal.
        if all(i == X[0] for i in X):
            return 0
        elif all(i == Y[0] for i in Y):
            return 90
        
        return -1
    