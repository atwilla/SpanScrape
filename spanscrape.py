from bs4 import BeautifulSoup as BS
import requests
import sys
import urllib3

verbose = False

if "-v" in sys.argv:
	vIndex = sys.argv.index("-v")
	verbose = True

	if vIndex == 1:
		word = ' '.join(sys.argv[2:])
	else:
		word = ' '.join(sys.argv[1:vIndex])
else:
	word = ' '.join(sys.argv[1:])

# print(word)

url = "https://spanishdict.com/translate/"

try:
	page = requests.get(url + word)
	soup = BS(page.text, 'html.parser')

	if verbose:
		headers = soup.find_all("div", class_="entry--3tNUi")[:-1]
		transBlocks = []

		try:

			for header in headers:
				transBlocks += header.find_next_siblings("div")
			
			for block in transBlocks:
				# Print word type.
				print(block.contents[0].find("a").text)

				# All translation text save for title found in contents[1].
				translations = block.contents[1].contents

				for trans in translations:
					# Print word summary.
					sumSpans = trans.contents[0].find_all("span")
					sumTxt = ""

					for span in sumSpans:
						sumTxt += span.text

					print("\t" + sumTxt)
					
					transDiv = trans.contents[1].contents[0]
					neoDictTrans = transDiv.find("a", 
						class_="neodictTranslation--C2TP2")
					print("\t\t" + neoDictTrans.text)	

				print("")

		except AttributeError:
				pass
	else:
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
