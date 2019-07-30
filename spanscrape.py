from bs4 import BeautifulSoup as BS
import requests
import sys
import urllib3

word = sys.argv[1]
url = "https://spanishdict.com/translate/"

try:
	page = requests.get(url + word)
	soup = BS(page.text, 'html.parser')
	divList = soup.find_all("div", class_="inline--1nnau")[1:]
	defList = []

	for div in divList:
		defList.append(div.contents[0].text)

	if len(defList) == 0:
		print("No translation found.")

	else:

		for definition in defList:
			print(definition)

except (requests.exceptions.SSLError):
	print("Could not connect to %s!", (url + word))
	print("Check internet connection, or page does not exist.")
