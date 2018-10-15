class Crypto():
	def __init__(self, ticker_name, price):
		self.ticker = ticker_name
		self.price = price

	def get_ticker(self):
		return self.ticker

	def get_price(self):
		return self.price