import os, http.client, json
from dotenv import load_dotenv

# Used during the start.sh script and ran by Cron once a day
# It requests the access token from authentication provider so that the application server can trust it
# It is then saved in a .env file

def access_token_request(payload):
    conn = http.client.HTTPSConnection("dev-bnn5mo4vff0z34au.eu.auth0.com")
    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()

    decoded_data = data.decode("utf-8")
    parsed_data = json.loads(decoded_data)
    access_token = parsed_data.get("access_token")

    return access_token

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
