import os, http.client, json, ssl
from dotenv import load_dotenv

# Used during the start.sh script to request a location ID from the application server
# It is then saved in a .env file

def post_location(token, lon, lat):
    """
    In order to set a location ID, you need an access_token, longitude, and latitude
    """
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("192.168.137.3", 8080, context=context)
    
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
    }
    
    body = json.dumps({
        "lon": lon, # float
        "lat": lat # float
    })
    
    try:
        conn.request("POST", "/api/location", body=body, headers=headers)
        response = conn.getresponse()
        data = response.read()
        print("Response:", response.status, data.decode("utf-8"))

        parsed_data = json.loads(data.decode("utf-8"))

        return parsed_data['locationId']
    except Exception as e:
        print(f"Error sending data: {e}")
        return None

if __name__ == "__main__":
    load_dotenv(".env")
    token = os.getenv("access_token")
    lon = 4.987
    lat = 51.159

    loc_id = post_location(token, lon, lat)
    print(loc_id)

    lines = []
    with open('.env','r') as f:
        for l in f:
            lines.append(l.split('='))

    print(lines)
    with open('.env','w') as f:
        for l in lines:
            if l[0] == "loc_id":
                f.write("loc_id=" + loc_id + '\n')
            else:
                f.write(l[0] + '=' + l[1])