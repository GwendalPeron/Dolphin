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

    def getPortfolioSharpe(self):
        qry = "/ratio/invoke"
        body = json.dumps({
                           "ratio":[self.RATIO_SHARPE],
                           "asset":[self.portfolio],
                           "bench":None,
                           "startDate":self.PERIOD_START_DATE,
                           "endDate":self.PERIOD_END_DATE,
                           "frequency":None
                           })
        url = self.url + qry
        r = requests.post(url, data=body, auth=self.auth, verify=False)
        data = json.loads(r) # TODO maybe useless
        return data[str(self.portfolio)][str(self.RATIO_SHARPE)]["value"]


    # TODO Untested 404
    def getRatios(self, id):
        qry = "/ratio/invoke"
        body = json.dumps({
                           "ratio":[self.RATIO_VOLATILIY, self.RATIO_SHARPE, self.RATIO_PERFORMANCE],
                           "asset":[id],
                           "bench":None,
                           "startDate":self.PERIOD_START_DATE,
                           "endDate":self.PERIOD_END_DATE,
                           "frequency":None
                           })
        url = self.url + qry
        r = requests.post(self.url, data=body, auth=self.auth, verify=False)
        return r

    # TODO Untested 404
    def getQuote(self, id):
        qry = ("/asset/" + str(id) + "/quote" + "?start_date=" + self.PERIOD_START_DATE + "&end_date=" + self.PERIOD_END_DATE)
        r = requests.get(self.url, auth=self.auth, verify=False)
        return r

    # TODO Untested 404
    def get_n_best_sharpes(n, ratios):
        vals = []
        for key, value in ratios: # key is asset id
            vals.append((key, value[str(self.RATIO_SHARPE)]["value"])) # append id, sharpe tuple
        vals = sorted(vals, key=lambda x: x[1]) # Sort by value
        return vals[:n]


a = APIWhisperer()
#a.getQuote(263)
#print(a.getRatios(263))
#print(a.getAssetList())
