from stock import Stock
import sys

ticker = raw_input('Enter ticker symbol: ').lower()
stock = Stock(ticker)
print 'Quote:', stock.get_quote()
print 'Market Cap:', stock.get_market_cap()
print 'P/E Ratio:', stock.get_pe_ratio()
print 'EBITDA:', stock.get_ebitda()
print 'FCF:', stock.get_fcf()

# wilshire = open('ticker.txt', 'r')
# error = open('error.txt', 'w')
# for ticker in wilshire:
# 	try:
# 		stock = Stock(ticker)
# 		stock.get_fcf()
# 	except:
# 		print ticker
# 		error.write(ticker)
# error.close()