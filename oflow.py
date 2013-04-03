#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
from urllib import quote
import json
import gzip
import sys
from StringIO import StringIO
from optparse import OptionParser

GOOGLE_QUERY = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&' + \
             'q=site:stackoverflow.com%2Fquestions+' + \
             '-%22stackoverflow.com%2Fquestions%2Ftagged%22+'

STACKOVERFLOW_QUERY = "https://api.stackexchange.com/2.1/questions/%s?order=desc&sort=votes&site=stackoverflow" + \
					  "&filter=!u1lUe2P33j_dkzJ6wiGGgDqpH)LCKtF" + \
					  "&key=hZMI)X9ibfxB2*5zSIbLlw(("

def google_search(query):
	data = urllib2.urlopen(GOOGLE_QUERY+quote(query))
	data = json.load(data)
	return [result['url'] for result in data['responseData']['results']]

def get_question_json(question_id):
	so_url = STACKOVERFLOW_QUERY % question_id
	request = urllib2.Request(so_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
		result = json.loads(data)
	return result['items']

def extract_pre_blocks(html):
	return [code.get_text().strip() for code in BeautifulSoup(html).find_all('pre')]

def print_q_and_a((question,answer)):
	question_info = "######## [ %s votes ] %s ########" % (answer['up_vote_count'],question['title'])
	pre_blocks = extract_pre_blocks(answer['body'])
	width = len(question_info)
	print "#" * width
	print question_info
	print "#" * width
	print "\n" + "\n\n########\n\n".join(pre_blocks) + "\n"

def a_contains_code(QA):
	return len(extract_pre_blocks(QA[1]['body'])) > 0

def oflow_query(query):
	urls = google_search(query)

	# extract the question ID's from the full URL's
	question_ids = [url.split('/')[4] for url in urls]

	# get all the question-answer pairs
	QAs = []
	for q_id in question_ids:
		# get question json data from api.stackexchange.com
		q_json = get_question_json(q_id)
		if len(q_json) == 0:
			# question was probably deleted, so go to next question
			continue
		q_json = q_json[0]
		# check that there were answers
		if q_json.has_key('answers'):
			QAs = QAs + [(q_json,answer) for answer in q_json['answers']]

	# pick QAs with code
	code_QAs = filter(a_contains_code, QAs)

	# sort QAs by answer['up_vote_count']
	sorted_QAs = sorted(code_QAs, key = lambda x: int(x[1]['up_vote_count']), reverse=True)
	
	return sorted_QAs


# if run as script:
if __name__ == "__main__":
	
	# parse commandline arguments
	usage = "oflow.py [options] query"
	parser = OptionParser(usage = usage)
	parser.add_option("-n", "--number", dest="n", default=5,
										help="number of results to display [default: %default]", metavar="N", type="int")
	(options, args) = parser.parse_args()
	if len(args) == 0:
		print(usage)
		sys.exit(2)

	# google stackoverflow for some phrase
	N = options.n
	query = " ".join(args)

	sorted_QAs = oflow_query(query)

	# print top N QAs
	for i in reversed(range(min(N,len(sorted_QAs)))):
		print_q_and_a(sorted_QAs[i])
