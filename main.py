from stock import Stock
import sys

# ticker = raw_input('Enter ticker symbol: ').upper()
# stock = Stock(ticker)

index = open('index/dow_jones.txt', 'r')
for ticker in index:
	stock = Stock(ticker)