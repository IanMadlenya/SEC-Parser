from stock import Stock
import sys
import time

# ticker = raw_input('Enter ticker symbol: ').upper()
# stock = Stock(ticker)
# print 'Quote:', stock.get_quote()
# print 'Market Cap:', stock.get_market_cap()
# print 'P/E Ratio:', stock.get_pe_ratio()
# print 'P/B Ratio:', stock.get_pb_ratio()
# print 'EBITDA:', stock.get_ebitda()
# print 'FCF:', stock.get_fcf()

index = open('sp500.txt', 'r')
for ticker in index:
	stock = Stock(ticker)
	print stock.get_ticker(), stock.get_fcf()