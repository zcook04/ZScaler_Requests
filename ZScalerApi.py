import time, json, requests
from os import getenv
from dotenv import load_dotenv

#Load Environmental Variables In .env File
load_dotenv('.env')

class ZScalerApi():
    def __init__(self):
        self.timestamp, self.api_key = self.obfuscateApiKey()
        self.url = getenv('ZSCALER_URL')
        self.username = getenv('ZSCALER_USERNAME')
        self.password = getenv('ZSCALER_PASSWORD')
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
        payload = {
            'username': self.username,
            'password': self.password,
            'apiKey': self.api_key,
            'timestamp': self.timestamp
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


    def _send_post_request(self, url):
        return self.session.post(self.url+url).json()

    def get_admin_users(self):
        return self._send_get_request('/adminUsers')

    def get_admin_roles(self):
        return self._send_get_request('/adminRoles/lite')

    def get_activation_status(self):
        return self._send_get_request('/status')

    def get_admin_audit_log(self):
        return self._send_get_request('/auditlogEntryReport')

    def get_authenticated_session(self):
        return self._send_get_request('/authenticatedSession')

    def get_firewall_rules(self):
        return self._send_get_request('/firewallFilteringRules')

    def get_locations(self):
        return self._send_get_request('/locations')
    
    def get_locations_lite(self):
        return self._send_get_request('/locations/lite')

    def get_location_by_id(self, id):
        return self._send_get_request(f'/locations/{id}')

    def get_locations_groups(self):
        return self._send_get_request('/locations/groups')
    
    def get_locations_groups_lite(self):
        return self._send_get_request('/locations/groups/lite')

    def get_location_groups_by_id(self, id):
        return self._send_get_request(f'/locations/groups/{id}')

    def get_white_list_urls(self):
        '''Returns a list of white-listed URLS'''
        return self._send_get_request('/security')

    def post_activation(self):
        return self._send_post_request('/status/activate')


