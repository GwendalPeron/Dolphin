import json
import requests
from requests.auth import HTTPBasicAuth


class APIWhisperer:
    def __init__(self):
        self.url = 'https://dolphin.jump-technology.com:3389/api/v1'
        self.username = "epita_user_2"
        self.password = "dolphin39355"
        self.auth = (self.username, self.password)
        self.portfolio = 567
        self.PERIOD_START_DATE = "2012-01-01"
        self.PERIOD_END_DATE = "2017-06-30"
        self.MIN_NAV_PER_LINE = 0.01
        self.MAX_NAV_PER_LINE = 0.1
        self.RATIO_PERFORMANCE = 21
        self.RATIO_VOLATILIY = 18
        self.RATIO_SHARPE = 20

    def getAssetList(self):
        qry = ("/asset?columns=ASSET_DATABASE_ID"
               "&columns=CURRENCY"
               "&columns=LABEL"
               "&columns=TYPE"
               "&columns=LAST_CLOSE_VALUE_IN_CURR"
               "&date=2012-01-01"
               "&CURRENCY=EUR")
        url = self.url + qry
        r = requests.get(url, auth=self.auth, verify=False)
        return r

    def getPortfolio(self):
        qry = "/portfolio/" + self.portfolio + "/dyn_amount_compo"
        url = self.url + qry
        r = requests.get(url, auth=self.auth, verify=False)
        return r

    # Untested 404
    def getRatios(self, id):
        qry = "/ratio/invoke"
        body = json.dumps({
                           "ratio":[self.RATIO_VOLATILIY, self.RATIO_SHARPE, self.RATIO_PERFORMANCE],
                           "asset":[id],
                           "bench":null,
                           "startDate":"2012-01-01",
                           "endDate":"2017-06-30",
                           "frequency":null
                           })
        r = requests.post(url, data=body, auth=self.auth, verify=False)
        return r

a = APIWhisperer()
print(a.getAssetList())
