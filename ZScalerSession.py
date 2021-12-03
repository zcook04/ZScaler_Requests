import time, json, requests
from os import getenv
from dotenv import load_dotenv

#Load Environmental Variables In .env File
load_dotenv('.env')

class ZScalerSession():
    def __init__(self):
        self.url = getenv('ZSCALER_URL')
        self.session = self.login()
 
    def obfuscateApiKey (self):
        seed = getenv('ZSCALER_API')
        time_now = int(time.time() * 1000)
        n = str(time_now)[-6:]
        r = str(int(n) >> 1).zfill(6)
        obf_key = ""
        for i in range(0, len(str(n)), 1):
            obf_key += seed[int(str(n)[i])]
        for j in range(0, len(str(r)), 1):
            obf_key += seed[int(str(r)[j]) + 2]

        return time_now, obf_key

    def login(self):
        session = requests.Session()
        timestamp, api_key = self.obfuscateApiKey()
        payload = {
            'username': getenv('ZSCALER_USERNAME'),
            'password': getenv('ZSCALER_PASSWORD'),
            'apiKey': api_key,
            'timestamp': timestamp
        }
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }
        res = session.post(self.url + '/authenticatedSession', data=json.dumps(payload), headers=headers)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error Authenticating.  Expected 200OK. Error: {e}"
        return session

    def _send_get_request(self, url):
        res = self.session.get(self.url+url)
        if res.status_code == 200:
            return res.json()
        else:
            print(f'An error occured getting to: {url}')