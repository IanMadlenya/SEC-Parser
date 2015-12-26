from yahoo_finance import Share
from bs4 import BeautifulSoup
# from parser import *
import urllib
import re

class Stock:
	def __init__(self, ticker):
		self.ticker = ticker.rstrip().upper()
		self.quote = None
		self.market_cap = None
		self.ev = None
		self.pe_ratio = None
		self.pb_ratio = None
		self.ebitda = None
		self.fcf = None

	def get_ticker(self):
		return self.ticker

	def get_quote(self):
		if self.quote is not None:
			return self.quote
		self.quote = float(Share(self.ticker).get_price())
		return self.quote

	def get_market_cap(self):
		if self.market_cap is not None:
			return self.market_cap

		market_cap = Share(self.ticker).get_market_cap()
		if market_cap is not None:
			self.market_cap = float(market_cap[:-1]) * (10**6 if 'M' in market_cap[-1] else 10**9)
			return self.market_cap

	def get_ev(self):
		if self.ev is not None:
			return self.ev

		url = 'https://ycharts.com/companies/' + self.ticker + '/enterprise_value'
		soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

		try:
			ev = soup.find('meta', content=re.compile('.*Enterprise Value.*'))['content']
			ev = ev[ev.index('of ') + 3 : ev.index('. ')]
			self.ev = float(ev[:-1]) * (10**6 if 'M' in ev[-1] else 10**9)
			return self.ev
		except:
			return None

	def get_pe_ratio(self):
		if self.pe_ratio is not None:
			return self.pe_ratio

		url = 'https://ycharts.com/companies/' + self.ticker + '/pe_ratio'
		soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

		try:
			pe_ratio = soup.find('meta', content=re.compile('.*PE Ratio.*'))['content']
			pe_ratio = pe_ratio[pe_ratio.index('of ') + 3 : pe_ratio.index('. ')]
			self.pe_ratio = float(pe_ratio)
			return self.pe_ratio
		except:
			return None

		# self.pe_ratio = float(Share(self.ticker).get_price_earnings_ratio())
		# return self.pe_ratio

	def get_pb_ratio(self):
		if self.pb_ratio is not None:
			return self.pb_ratio
		self.pb_ratio = float(Share(self.ticker).get_price_book())
		return self.pb_ratio

	def get_ebitda(self):
		if self.ebitda is not None:
			return self.ebitda

		ebitda = Share(self.ticker).get_ebitda()
		if ebitda is not None:
			self.ebitda = float(ebitda[:-1]) * (10**6 if 'M' in ebitda[-1] else 10**9)
			return self.ebitda

	def get_fcf(self):
		if self.fcf is not None:
			return self.fcf

		url = 'https://ycharts.com/companies/' + self.ticker + '/free_cash_flow'
		soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

		try:
			fcf = soup.find('meta', content=re.compile('.*Free Cash Flow.*'))['content']
			fcf = fcf[fcf.index('of ') + 3 : fcf.index('. ')]
			self.fcf = float(fcf[:-1]) * (10**6 if 'M' in fcf[-1] else 10**9)
			return self.fcf
		except:
			return None

		# if self.fcf is not None:
		# 	return self.fcf

		# try:
		# 	soup = get_statements(self.ticker)
		# 	self.income_statement = soup[0][0]
		# 	self.balance_sheet = soup[1][0]
		# 	self.cash_flow_statement = soup[2][0]

		# 	a = parse_statement(self.income_statement, [['_OperatingIncomeLoss'], ['_IncofcfxExpenseBenefit'], ['_IncomeLossFromContinuingOperationsBeforeIncofcfxes'], ['_InterestExpense'], ['_DepreciationAndAmortization', '_DepreciationDepletionAndAmortization']], soup[0][1])
		# 	b = parse_statement(self.balance_sheet, [['_AssetsCurrent'], ['_LiabilitiesCurrent\'']], soup[1][1])
		# 	c = parse_statement(self.cash_flow_statement, [['_DepreciationAndAmortization', '_DepreciationDepletionAndAmortization', '_DepreciationAmortizationAndAccretionNet', '_DepreciationAmortizationAndOther', '_OtherDepreciationAndAmortization'], ['_Depreciation'], ['_Amortization'], ['_PaymentsToAcquirePropertyPlantAndEquipment', '_PaymentsToAcquireProductiveAssets']], soup[2][1])

		# 	if a[0] is None:
		# 		a[0] = a[2] if a[3] is None else a[2] + a[3]
		# 	if a[4] is None:
		# 		a[4] = c[0] if c[0] is not None else (c[1] if c[1] is not None else 0) + (c[2] if c[2] is not None else 0)
		# except ValueError:
		# 	return 'missing 10-k report'
		# except TypeError:
		# 	return 'missing financial statement'

		# try:
		# 	# print a
		# 	# print b
		# 	# print c
			
		# 	return a[0] * (1 - a[1] / a[2]) + a[4] - (b[0] - b[1]) - abs(c[3])
		# except TypeError:
		# 	return None
		# 	# return 'missing data'