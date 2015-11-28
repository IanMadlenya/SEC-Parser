from bs4 import BeautifulSoup
import sys
import urllib
import re
import unicodedata

def parse_statement(statement, query, multiplier):
	values = [None] * len(query)
	all_entries = statement.find_all('tr', {'class':['re', 'ro', 'reu', 'rou', 'rh']})
	for entry in all_entries:
		if None not in values:
			break

		title = entry.find('a', class_='a')
		if title is None:
			continue
		else:
			title = title.get('onclick')

		numbers = entry.find_all('td', {'class':['nump', 'num']})
		for i in range(0, len(query)):
			for j in range(0, len(query[i])):
				if query[i][j] in title:
					values[i] = 0 if not numbers else float(parse_amount(numbers[0].get_text())) * multiplier
					break
			else:
				continue
			break

	return values

def get_statements(ticker):
	url = get_url(ticker)
	if url is None:
		raise ValueError('missing 10-k report')

	soup = [None] * 3
	soup[0] = (BeautifulSoup(urllib.urlopen(url[0][0]).read(), 'lxml'), url[0][1])
	soup[1] = (BeautifulSoup(urllib.urlopen(url[1][0]).read(), 'lxml'), url[1][1])
	soup[2] = (BeautifulSoup(urllib.urlopen(url[2][0]).read(), 'lxml'), url[2][1])
	return soup

def get_url(ticker):
	url1 = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='
	url2 = '&owner=exclude&action=getcompany&Find=Search&type=10-k'

	url = url1 + ticker + url2
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	cik = get_cik_no(soup)
	acc = get_acc_no(soup)
	if cik is None or acc is None:
		return None # missing 10-k report

	report = [None] * 3
	url = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' + acc + '/R'
	for page in range(2, 13):
		if None not in report:
			break
		statement = url + str(page) + '.htm'
		soup = BeautifulSoup(urllib.urlopen(statement).read(), 'lxml')

		# print statement
		try:
			title = soup.find('th', class_='tl').get_text().lower()
		except AttributeError:
			return None # missing interactive data

		if report[0] is None and is_income_statement(title):
			title = re.compile(',').split(title)
			for phrase in title:
				if len(title) is not 1 and 'share' in phrase.lower():
					continue
				if 'thousand' in phrase.lower():
					report[0] = (statement, 10**3)
				elif 'million' in phrase.lower():
					report[0] = (statement, 10**6)
				elif 'billion' in phrase.lower():
					report[0] = (statement, 10**9)
				else:
					report[0] = (statement, 1)
		if report[1] is None and is_balance_sheet(title):
			report[1] = (statement, 10**3 if 'thousand' in title else 10**6 if 'million' in title else 10**9)
		if report[2] is None and is_cash_flow_statement(title):
			report[2] = (statement, 10**3 if 'thousand' in title else 10**6 if 'million' in title else 10**9)

	return report

def get_cik_no(soup):
	span = soup.find('span', class_='companyName')
	if span is None:
		return None

	cik = re.sub(r'\D', '', span.a.get_text())
	for i in range(0, len(cik)):
		if cik[i] != '0':
			return cik[i:]

def get_acc_no(soup):
	tr = soup.find_all('tr')
	for i in tr:
		report_type = i.find('a', id='interactiveDataBtn')
		if report_type is not None:
			return parse_acc_no(i.find('td', class_='small'))

def parse_acc_no(acc_no):
	acc = 'Acc-no: '
	acc_index = acc_no.get_text().index(acc)
	acc_length = 20
	
	return acc_no.get_text()[acc_index + len(acc) : acc_index + len(acc) + acc_length].replace('-', '')

def parse_amount(amount):
	amount = re.sub(r'[^\(\d]', '', amount)
	amount = amount.replace('(', '-')
	amount = unicodedata.normalize('NFKD', amount).encode('ascii','ignore')
	return amount

def is_income_statement(title):
	if 'parenthetical' in title:
		return False

	keywords = ['operation', 'income', 'earning', 'loss']
	for word in keywords:
		if word in title:
			return True
	return False

def is_balance_sheet(title):
	if 'parenthetical' in title:
		return False

	keywords = ['balance sheet', 'financial position', 'financial condition', 'condition', 'assets', 'liabilities']
	for word in keywords:
		if word in title:
			return True
	return False

def is_cash_flow_statement(title):
	return 'cash' in title and 'flow' in title and not 'parenthetical' in 'title'