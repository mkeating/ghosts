from bs4 import BeautifulSoup
import urllib2
from random import randint
from twitter import *

CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'
OAUTH_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXX'
OAUTH_TOKEN_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'

t = Twitter(
			auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
					CONSUMER_KEY, CONSUMER_SECRET))


lucky_winner = randint(1,503)

base_url = "http://www.tdcj.state.tx.us/stat/"

response = urllib2.urlopen(base_url+'dr_executed_offenders.html')
base_html = response.read()
soup = BeautifulSoup(base_html)

table = soup.table
rows = table.findAll("tr")
prisoner = rows[503 - lucky_winner+1]

statement_url = base_url +  prisoner.find_all('a', text="Last Statement")[0]['href']

statement_html = urllib2.urlopen(statement_url).read()
soup = BeautifulSoup(statement_html)

statement = soup.find_all('p',  {'id': '',  'class': ''})[2:]

def chunks(s,n):
	for start in range(0, len(s), n):
		yield s[start:start+n]

if statement:

	selection = statement[randint(0, len(statement)-1)]


	if len(selection.text) < 140:
		print selection.text
		t.statuses.update(status=selection.text)
	else:
		final = []
		for chunk in chunks(selection.text, 130):
			final.append(chunk)
		for e in final:
			if final.index(e) != -1:
				e = e + " (cont)"
		for e in reversed(final):
			print final.index(e)
			print e
			#t.statuses.update(status=e)
else:
	print 'No Last Statement'
	#t.statuses.update(status='No Last Statement')
	


