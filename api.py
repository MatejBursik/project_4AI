import http.client
import json
 
conn = http.client.HTTPSConnection("dev-bnn5mo4vff0z34au.eu.auth0.com")
 
payload = "{\"client_id\":\"8hR25ciTaviKwOVYajMlbshDCBK4wTOv\",\"client_secret\":\"0bRdmCr6YH-fegEA_Bx06il0-EOTKUyAa8p-SOKxpY8wpXFJzBud-Hl5ORm6izEI\",\"audience\":\"https://nestquestproject\",\"grant_type\":\"client_credentials\"}"
 
headers = { 'content-type': "application/json" }
 
conn.request("POST", "/oauth/token", payload, headers)
 
res = conn.getresponse()
data = res.read()
 
decoded_data = data.decode("utf-8")
 
parsed_data = json.loads(decoded_data)
 
# Step 3: Access the `access_token` attribute
access_token = parsed_data.get("access_token")