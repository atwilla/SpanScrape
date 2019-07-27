from bs4 import BeautifulSoup as BS
import requests
import sys
import urllib3

word = sys.argv[1]
url = "https://spanishdict.com/"

try:
	page = requests.get(url + word)
	soup = BS(page)
except (requests.exceptions.SSLError):
	print("Could not connect to SpanishDict.com!")
