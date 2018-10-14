import urllib2
import json

class CryptoCompareClient():
	def __init__(self):
		self.price_request_url = "https://min-api.cryptocompare.com/data/price?fsym="


	def request_price(self, crypto, currency):
		request_url = self.price_request_url+"%s&tsyms=%s"%(crypto, currency)
		response = self.make_request(request_url)
		if response != None and currency in response:
			return response[currency]
		return 0.0

	def make_request(self, request_url):
		response = json.loads(urllib2.urlopen(request_url).read())
		if response == None or "Response" in response and response["Response"] == "Error":
			 return None
		else:
			return response