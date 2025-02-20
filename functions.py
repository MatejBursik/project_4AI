import requests, cv2, numpy as np, http.client, json, time, ssl
from sklearn.linear_model import LinearRegression

def app_send_data(token, loc_id, color, enter_or_exit, angle):
    """
    This function does a post request to the application server.
    It sends log data about the Asian hornet sighting.
    """
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("192.168.137.3", 8080, context=context)
    
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
    }
    
    body = json.dumps({
        "direction": angle,
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "locationId": loc_id,
        "isMarked": False if color == 'black' else True,
        "color": color,
        "isIncoming": True if enter_or_exit == 'enter' else False,
        "isManual": False
    })
    
    try:
        conn.request("POST", "/api/log", body=body, headers=headers)
        response = conn.getresponse()
        data = response.read()
        print("Response:", response.status, data.decode("utf-8"))
    except Exception as e:
        print(f"Error sending data: {e}")

def run_request(run):
    """
    This function does a local post request to change the status on the relay (ON/OFF)
    """
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
            print("Response:", response.status, data.decode("utf-8"))

    except Exception as e:
        print(f"An error occurred: {e}")

def draw_rect_with_label(x1, y1, x2, y2, frame, label, color = (0, 0, 255)):
    """
    Draw a rectangle and a label onto a frame.
    Return the labelled frame
    """
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def draw_circle(x1, y1, x2, y2, frame, color = (0, 0, 255)):
    """
    Draw a filled in circle onto a frame.
    Return the labelled frame
    """
    cv2.circle(frame, (int(x1+((x2-x1)/2)), int(y1+((y2-y1)/2))), 15, color, -1)
    return frame

def identify_color(image):
    """
    This function identifies the dominant color in the region out of a preset colors.
    The preset colors at the moment are "red", "blue", "pink".
    It returns the mean rgb value of the color and a string representation of the color.
    """
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

        # If the new mask covers more of the image, update the color_mask and color
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

def midpoint(x1, y1, x2, y2):
    """
    Calculates the middle point of two point.
    Returns the coordinate of this point.
    """
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2
    return (x_mid, y_mid)

def direction(X, Y):
    """
    This function determines the motion direction based on the sets of X and Y coordinates.
    Returns the string representation of the direction.
    To better understand the return string, follow the comments in the code.
    """
    lr = "" # Left or Right
    ud = "" # Up or Down

    if Y[0] > Y[-1]: # Slope negative
        if X[0] > X[-1]: # Right
            lr = "r"
            ud = "d"
        elif X[0] < X[-1]: # Left
            lr = "l"
            ud = "d"
    elif Y[0] < Y[-1]: # Slope positive
        if X[0] > X[-1]: # Right
            lr = "r"
            ud = "u"
        elif X[0] < X[-1]: # Left
            lr = "l"
            ud = "u"
    else:
        # If the fligh path is perfectly horizontal or vertical
        # the magnitude/slope is 0 and can not determine which it is
        # so it needs to be determined by the points. If all X values
        # are the same then it is perfectly vertical and if all Y values
        # are the same then it is perfectly horizontal.
        # If they are perfectly vertical or horizontal, they equal to p
        if all(i == X[0] for i in X): # all X values are the same = perfectly vertical
            lr = "p"
            if Y[0] > Y[-1]: # Down
                ud = "d"
            elif Y[0] < Y[-1]: # Up
                ud = "u"
        elif all(i == Y[0] for i in Y): # all Y values are the same = perfectly horizontal
            ud = "p"
            if X[0] > X[-1]: # Right
                lr = "r"
            elif X[0] < X[-1]: # Left
                lr = "l"
        else:
            return -1
        
    return lr + ud

def enter_exit_calc(coord_1, coord_2, coord_3):
    """
    Calculates the enter or exit direction relative to the screens north.
    This is calculated from 3 coordicates provided from the AI predictions over 3 frames.
    It returns the angle.
    """
    X = np.array([coord_1[0], coord_2[0], coord_3[0]])
    Y = np.array([coord_1[1], coord_2[1], coord_3[1]])

    # Train model
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), Y)

    m = model.coef_[0] # Slope of the best-fit line
    screen_m = 0 # Horizontal slope of the screen
    print("m",m)

    # Check for perpendicular lines
    if (m * screen_m) == -1:
        angle = 90.0
    else:
        # Compute the angle in radians
        angle_radians = np.arctan(abs((m - screen_m) / (1 + m * screen_m)))
        angle = np.degrees(angle_radians)

    vec_direction = direction(X, Y)
    print(vec_direction)
    match vec_direction:
        case 'rd':
            angle = 90 + angle
        case 'ru':
            angle = abs(angle - 90)
        case 'rp':
            angle = 90
        case 'ld':
            angle = 270 - angle
        case 'lu':
            angle = 270 + angle
        case 'lp':
            angle = 270
        case 'pd':
            angle = 180
        case 'pu':
            angle = 0
        case -1 | '' | _:
            return -1   

    # Return angle relative to the screen north
    return angle

def most_frequent_color(words):
    """
    Returns the most frequent word (color) from a list of strings.
    """
    if not words:
        return None
    
    # Count occurrences using dictionary comprehension
    word_counts = {word: words.count(word) for word in set(words)}
    
    # Find the word with the maximum count
    return max(word_counts, key=word_counts.get)
