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

	def request_historical(self, crypto, currency, limit):
		request_url = "https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=%s&limit=%s&e=CCCAGG"%(crypto, currency, limit)
		response = self.make_request(request_url)
		if response != None:
			return _extract_historical_prices(response['Data'])
		return None


	def make_request(self, request_url):
		response = json.loads(urllib2.urlopen(request_url).read())
		if response == None or "Response" in response and response["Response"] == "Error":
			 return None
		else:
			return response

	def __extract_historical_prices(ticker_list):
		if ticker_list != None:
			return [ record['close'] for record in ticker_list ]
		return None