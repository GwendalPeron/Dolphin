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
        qry = "/portfolio/" + str(self.portfolio) + "/dyn_amount_compo"
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
        data = json.loads(r.content)
        return data[str(self.portfolio)][str(self.RATIO_SHARPE)]["value"]

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
        r = requests.post(url, data=body, auth=self.auth, verify=False)
        return r

    def getQuote(self, id):
        qry = ("/asset/" + str(id) + "/quote" + "?start_date=" + self.PERIOD_START_DATE + "&end_date=" + self.PERIOD_END_DATE)
        url = self.url + qry
        r = requests.get(url, auth=self.auth, verify=False)
        return r

    def getNBestSharpe(self, n):
        assets = json.loads(self.getAssetList().content)
        ids = [a["ASSET_DATABASE_ID"]["value"] for a in assets]
        sharpes = self.getMultipleAssetSharpe(ids)
        vals = sorted(sharpes, key=lambda x: x[1], reverse=True) # Sort by value
        return vals[:n]

    def getAssetSharpe(self, id):
        qry = "/ratio/invoke"
        body = json.dumps({
                           "ratio":[self.RATIO_SHARPE],
                           "asset":[id],
                           "bench":None,
                           "startDate":self.PERIOD_START_DATE,
                           "endDate":self.PERIOD_END_DATE,
                           "frequency":None
                           })
        url = self.url + qry
        r = requests.post(url, data=body, auth=self.auth, verify=False)
        data = json.loads(r.content)
        return data[str(id)][str(self.RATIO_SHARPE)]["value"]

    def getMultipleAssetSharpe(self, ids):
        qry = "/ratio/invoke"
        body = json.dumps({
                           "ratio":[self.RATIO_SHARPE],
                           "asset":ids,
                           "bench":None,
                           "startDate":self.PERIOD_START_DATE,
                           "endDate":self.PERIOD_END_DATE,
                           "frequency":None
                           })
        url = self.url + qry
        r = requests.post(url, data=body, auth=self.auth, verify=False)
        data = json.loads(r.content)
        sharpes = [(asset, data[asset][str(self.RATIO_SHARPE)]["value"]) for asset in data]
        return sharpes

    def getAssetPrice(self, id):
        qry = ("/asset/" + str(id) + "/quote" + "?start_date=" + "2011-12-30" + "&end_date=" + self.PERIOD_START_DATE)
        url = self.url + qry
        r = requests.get(url, auth=self.auth, verify=False)
        data = json.loads(r.content)
        price = data[0]["nav"]
        return price

    def putPortfolio(self, weightedAssets):
        ids, weights = weightedAssets # expected : [(42, 0.06), (46, 0.1)] etc : id-weight tuples
        # TODO

a = APIWhisperer()
#print(a.getAssetList().content)
#print(a.getPortfolio().content)
#print(a.getPortfolioSharpe())
#print(a.getRatios(263).content)
#print(a.getQuote(263).content)
#print(a.getAssetSharpe(263))
#print(a.getMultipleAssetSharpe([263, 405]))
#print(a.getNBestSharpe(20))
print(a.getAssetPrice(54))
