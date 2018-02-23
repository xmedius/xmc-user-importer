import requests

class Client:
    def __init__(self, access_token, enterprise_account, endpoint='https://portal.xmedius.com'):
        self.access_token = str(access_token)
        self.enterprise_account = enterprise_account
        self.endpoint = endpoint

    def default_group(self):
        groups_result = self._groups()
        return groups_result['default']

    def groups(self):
        groups_result = self._groups()
        return groups_result['groups']

    def fax_numbers(self):
        url = "%s/enterprises/%s/fax_numbers" % (self.endpoint, self.enterprise_account)
        r = requests.get(url, headers=self._portal_headers() )
        json = r.json()

        if json['result'] == True:
            return json['data']['fax_numbers']
        else:
            raise RuntimeError("Error retrieving fax_numbers information")

    def add_user(self, user_parameters):
        #Remove unset keys to use the enterprise default
        if not user_parameters['language']:
            del user_parameters['language']

        if not user_parameters['time_zone']:
            del user_parameters['time_zone']

        data= { 'user': user_parameters }
        url = "%s/enterprises/%s/users" % (self.endpoint, self.enterprise_account)
        r = requests.post(url, headers=self._portal_headers(), json=data)
        return r.json()

    def _groups(self):
        url = "%s/enterprises/%s/groups" % (self.endpoint, self.enterprise_account)
        r = requests.get(url, headers=self._portal_headers() )
        json = r.json()

        if json['result'] == True:
            return json['data']
        else:
            raise RuntimeError("Error retrieving group information")

        return r.json()

    def _portal_headers(self):
        return { 'Authorization-Token': self.access_token,
                 'Content-type': "application/json",
                 'Accept': "application/json" }



