from functions import *
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")
    payload = os.getenv("payload")

    lines = []
    with open('.env','r') as f:
        for l in f:
            lines.append(l.split('='))

    print(lines)
    with open('.env','w') as f:
        for l in lines:
            if l[0] == "access_token":
                f.write("access_token=" + access_token_request(payload) + '\n')
            else:
                f.write(l[0] + '=' + l[1])
