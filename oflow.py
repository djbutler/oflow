from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
from urllib import quote
import json
import gzip
import sys
from StringIO import *

def google_search(query):
	data = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&q=site:stackoverflow.com+'+quote(query))
	data = json.load(data)
	return [result['url'] for result in data['responseData']['results']]

def get_answers(q_id):
	so_url = "https://api.stackexchange.com/2.1/questions/%s/answers?order=desc&sort=votes&site=stackoverflow&filter=!mjTUS_3xh." % q_id
	request = urllib2.Request(so_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO( response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
		result = json.loads(data)
	return [answer['body'] for answer in result['items']]

def get_codes(html):
	return [code.get_text() for code in BeautifulSoup(html).find_all('pre')]

query = sys.argv[1]
urls = google_search(query)
question_ids = [url.split('/')[4] for url in urls]

for i in range(len(question_ids)):
	q_id = question_ids[i]
	answer_list = get_answers(q_id)
	for answer in answer_list:
		codes = get_codes(answer)
		if len(codes) > 0:
			header = ("######## %s ########" % urls[i])
			print "#" * len(header)
			print header
			print "#" * len(header)
			print "\n####\n".join(codes)
