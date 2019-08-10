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


def printIndent(numTabs, text, charLim=80, tabLen=4):
	"""Print a large string with a consistent indentation without exceeding 
	   the specified char limit.
	"""

	tabs = ""

	for tab in range(numTabs):
		tabs += " " * tabLen

	words = [word + " " for word in text.split(" ")]
	words[-1] = words[-1][:-1]

	currLine = tabs

	for word in words:
		
		if len(currLine + word) <= charLim:
			currLine += word
		else:
			print(currLine)
			currLine = tabs + word

	if currLine != tabs:
		print(currLine)


def spanScrape(word, verbose=False):
	url = "https://spanishdict.com/translate/"
	
	try:
		page = requests.get(url + word)
		soup = BS(page.text, 'html.parser')
	
		if verbose:
			headers = soup.find_all("div", class_="entry--3tNUi")
			transTag = "neodictTranslation--C2TP2"
			contentBlocks = []
	
			try:
	
				for header in headers:
					contentBlocks += header.find_next_siblings("div")
				
				for block in contentBlocks:
	
					# All translation text save for title found in contents[1].
					translations = block.contents[1].contents

					# Check last translation for completeness. Trigger 
					# exception if incomplete to prevent printing a 
					# partial translation.
					lastTrans = translations[-1].contents[1].contents[0]
					lastTrans.find("a", class_=transTag).text

					wordType = block.contents[0].find("a").text
					print(wordType + "\n")
	
					for trans in translations:
						# Print word tags.
						tagSpans = trans.contents[0].find_all("span")
						tagTxt = ""
	
						for span in tagSpans:
							tagTxt += span.text
	
						printIndent(1, tagTxt + "\n")
						
						# transDiv holds translated words and example sentences.
						transDiv = trans.contents[1]

						neoDictTrans = [x.text for x in transDiv.find_all("a", 
							recursive=True, class_=transTag)]

						exSentences = [sentence.text for sentence in 
							transDiv.find_all("div", class_="indent--FyTYr")]

						for neoDict, sentence in zip(neoDictTrans, exSentences):
							printIndent(2, neoDict + "\n")	
							printIndent(3, sentence + "\n")
	
			except AttributeError:
				pass

		else:
			divList = soup.find_all("div", class_="inline--1nnau")[1:]
			transList = []
	
			for div in divList:
				transList.append(div.contents[0].text)
	
			if len(transList) == 0:
				print("No translation found.")
	
			else:
	
				for definition in defList:
					print(definition)
	
	except (requests.exceptions.SSLError):
		print("Could not connect to %s!", (url + word))
		print("Check internet connection, or page does not exist.")

spanScrape(word, verbose)
