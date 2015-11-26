from yahoo_finance import Share
from parser import *
import sys

class Stock:
	def __init__(self, ticker):
		self.ticker = ticker
		self.quote = None
		self.market_cap = None
		self.pe_ratio = None
		self.pb_ratio = None
		self.ebitda = None
		self.fcf = None

	def get_ticker(self):
		return self.ticker

	def get_quote(self):
		return Share(self.ticker).get_price() if self.quote is None else self.quote

	def get_market_cap(self):
		if self.market_cap is not None:
			return self.market_cap

		market_cap = Share(self.ticker).get_market_cap()
		if market_cap is not None:
			return float(market_cap[:-1]) * (10**6 if 'M' in market_cap[-1] else 10**9)

	def get_pe_ratio(self):
		return Share(self.ticker).get_price_earnings_ratio() if self.pe_ratio is None else self.pe_ratio

	def get_pb_ratio(self):
		return Share(self.ticker).get_price_book() if self.pb_ratio is None else self.pb_ratio

	def get_ebitda(self):
		if self.ebitda is not None:
			return self.ebitda

		ebitda = Share(self.ticker).get_ebitda()
		if ebitda is not None:
			return float(ebitda[:-1]) * (10**6 if 'M' in ebitda[-1] else 10**9)

	def get_fcf(self):
		if self.fcf is not None:
			return self.fcf

		try:
			soup = get_statements(self.ticker)
			self.income_statement = soup[0][0]
			self.balance_sheet = soup[1][0]
			self.cash_flow_statement = soup[2][0]

			a = parse_statement(self.income_statement, ['us-gaap_OperatingIncomeLoss\'', 'us-gaap_IncomeTaxExpenseBenefit\'', 'us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxes'], soup[0][1])
			b = parse_statement(self.balance_sheet, ['us-gaap_AssetsCurrent\'', 'us-gaap_LiabilitiesCurrent\''], soup[1][1])
			c = parse_statement(self.cash_flow_statement, ['us-gaap_PaymentsToAcquirePropertyPlantAndEquipment\''], soup[2][1])
		except ValueError:
			return 'missing 10-k report'
		except TypeError:
			return 'missing financial statement'

		try:
			# print a
			# print b
			# print c
			return a[0] * (1 - a[1] / a[2]) + (self.get_ebitda() - a[0]) - (b[0] - b[1]) - abs(c[0])
		except TypeError:
			return None
			# return 'missing data'