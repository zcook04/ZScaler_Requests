from ZScalerSession import ZScalerSession

class ZScalerRequest(ZScalerSession):
    def __init__(self):
        super().__init__()

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