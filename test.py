from bs4 import BeautifulSoup
import urllib
import sys
import re
import dateutil.parser

def get_price(ticker):
	url = 'https://ycharts.com/companies/' + ticker + '/price'
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	tr = soup.find('tr', class_='last')
	old_date = tr.find('td', class_='col1').get_text()
	old_price = float(tr.find('td', class_='col2').get_text())
	new_date = soup.find('td', class_='col1').get_text()
	new_price = float(soup.find('td', class_='col2').get_text())
	return old_date, old_price, new_date, new_price

def get_ev(ticker, old_date):
	url = 'https://ycharts.com/companies/' + ticker + '/enterprise_value'
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	try:
		ev = soup.find('meta', content=re.compile('.*Enterprise Value.*'))['content']
		ev = ev[ev.index('of ') + 3 : ev.index('. ')]
		ev = float(ev[:-1]) * (10**6 if 'M' in ev[-1] else 10**9)

		tr = soup.find_all('tr')
		for i in tr:
			date = i.find('td', class_='col1')
			if date is not None and date.get_text() == old_date:
				old_ev = i.find('td', class_='col2').get_text().strip()
				return float(old_ev[:-1]) * (10**6 if 'M' in old_ev[-1] else 10**9), ev
	except:
		return None

def get_fcf(ticker, old_date, new_date):
	url = 'https://ycharts.com/companies/' + ticker + '/free_cash_flow'
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	try:
		fcf = soup.find('meta', content=re.compile('.*Free Cash Flow.*'))['content']
		fcf = fcf[fcf.index('of ') + 3 : fcf.index('. ')]
		fcf = float(fcf[:-1]) * (10**6 if 'M' in fcf[-1] else 10**9)
		
		old_date = dateutil.parser.parse(old_date)
		new_date = dateutil.parser.parse(new_date)
		
		tr = soup.find_all('tr')
		for i in tr:
			date = i.find('td', class_='col1')
			if date is not None:
				date = dateutil.parser.parse(date.get_text())
				if (new_date - old_date).total_seconds() <= (new_date - date).total_seconds():
					old_fcf = i.find('td', class_='col2').get_text().strip()
					return float(old_fcf[:-1]) * (10**6 if 'M' in old_fcf[-1] else 10**9), fcf
	except:
		return None

def get_pe_ratio(ticker, old_date):
	url = 'https://ycharts.com/companies/' + ticker + '/pe_ratio'
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	try:
		pe_ratio = soup.find('meta', content=re.compile('.*PE Ratio.*'))['content']
		pe_ratio = float(pe_ratio[pe_ratio.index('of ') + 3 : pe_ratio.index('. ')])

		tr = soup.find_all('tr')
		for i in tr:
			date = i.find('td', class_='col1')
			if date is not None and date.get_text() == old_date:
				return float(i.find('td', class_='col2').get_text()), pe_ratio
	except:
		return None


index = open('index/nasdaq_100.txt', 'r')
stock = []
for ticker in index:
	try:
		ticker = ticker.rstrip().upper()
		old_date, old_price, new_date, new_price = get_price(ticker)

		old_ev, new_ev = get_ev(ticker, old_date)
		old_fcf, new_fcf = get_fcf(ticker, old_date, new_date)
		old_pe_ratio, new_pe_ratio = get_pe_ratio(ticker, old_date)

		old = (old_ev / old_fcf) / old_pe_ratio
		new = (new_ev / new_fcf) / new_pe_ratio

		# print new_price, new, " : ", old_price, old
		if new > old and new_price > old_price or new < old and new_price < old_price:
			stock.append((ticker, new, True))
		else:
			stock.append((ticker, new, False))

		print ticker
	except:
		pass

stock = sorted(stock, key=lambda x:x[1], reverse=True)
for s in stock:
	print s