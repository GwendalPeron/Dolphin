import requests
from requests.auth import HTTPBasicAuth


class Connec:
    def __init__(self):
        self.host = 'https://dolphin.jump-technology.com:3389/api/v1'
        self.user = 'epita_user_2'
        self.password = 'dolphin39355'

    def get_port(self, id):
        ext = '/portfolio/' + str(id) + '/dyn_amount_compo'
        url = self.host + ext
        print(url)
        return requests.get(url, auth=HTTPBasicAuth(self.user, self.password), verify=False)


    def put_port(self, id, data):
        ext = '/portfolio/' + str(id) + '/dyn_amount_compo'
        requests.put(self.host + ext , auth=self.auth, data=data)

    def get_list_ratio(self):
        ext = '/SCHEMA/ratio'
        return request.get(self.host + ext, auth=self.auth)

    def calc_ratio(self, data):
        ext = '/SCHEMA/ratio/invoke'
        return requests.post(self.host + ext, auth=self.auth, data=data)

    def get_cota_values(self, id):
        #date = 2017-06-01 (str)
        ext = 'SCHEMA/asset/' + str(id) + '/quote?start_date=2012-01-01&end_date=2017-06-01'
        return requests.get(self.host + ext, auth=self.auth)

    def get_base_act(self, date='2012-01-01'):
        ext = '/SCHEMA/asset?columns=ASSET_DATABASE_ID&columns=LABEL&columns=TYPE&columns=LAS T_CLOSE_VALUE_IN_CURR&date=' + date
        return requests.get(self.host + ext, auth=self.auth)


co = Connec()
resp = co.get_port(567)
print(resp.content)
