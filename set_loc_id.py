from functions import *
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")
    token = os.getenv("access_token")
    lon = 1.23
    lat = 4.56

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