from yahoo_finance import Share
from parser import parse
import sys

def get_quote(ticker):
	return Share(ticker).get_price()

def get_market_cap(ticker):
	market_cap = Share(ticker).get_market_cap()
	if market_cap is not None:
		return float(market_cap[:-1]) * (10**6 if 'M' in market_cap[-1] else 10**9)

def get_pe_ratio(ticker):
	return Share(ticker).get_price_earnings_ratio()

def get_ebitda(ticker):
	ebitda = Share(ticker).get_ebitda()
	if ebitda is not None:
		return float(ebitda[:-1]) * (10**6 if 'M' in ebitda[-1] else 10**9)

def get_fcf(ticker):
	try:
		num = parse(ticker)
		current_assets = num.next()
		ppe = num.next()
		current_liabilities = num.next()
	except ValueError:
		return 'missing 10-k report'
	except StopIteration:
		return 'missing fcf values'

	# print current_assets, current_liabilities, ppe
	if get_ebitda(ticker) is not None:
		return get_ebitda(ticker) - (current_assets - current_liabilities) - ppe

# ticker = raw_input('Enter ticker symbol: ').lower()
# # print 'Quote:', get_quote(ticker)
# # print 'Market Cap:', get_market_cap(ticker)
# # print 'P/E Ratio:', get_pe_ratio(ticker)
# # print 'EBITDA:', get_ebitda(ticker)
# print 'FCF:', get_fcf(ticker)

wilshire = open('ticker.txt', 'r')
error = open('error.txt', 'w')
for ticker in whilshire:
	try:
		fcf = get_fcf(ticker)
	except:
		print ticker
		error.write(ticker)
error.close()