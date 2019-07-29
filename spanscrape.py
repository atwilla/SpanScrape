from bs4 import BeautifulSoup as BS
import requests
import sys
import urllib3

word = sys.argv[1]
url = "https://spanishdict.com/translate/"

try:
	page = requests.get(url + word)
	soup = BS(page.text, 'html.parser')
	defList = soup.find_all("div", class_="inline--1nnau")[1:]

	for defn in defList:
		print(defn.contents[0].text)

except (requests.exceptions.SSLError):
	print("Could not connect to SpanishDict.com!")
