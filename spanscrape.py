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
			headers = soup.find_all("div", class_="entry--3tNUi")[:-1]
			transBlocks = []
	
			try:
	
				for header in headers:
					transBlocks += header.find_next_siblings("div")
				
				for block in transBlocks:
					# Print word type.
					print(block.contents[0].find("a").text + "\n")
	
					# All translation text save for title found in contents[1].
					translations = block.contents[1].contents
	
					for trans in translations:
						# Print word summary.
						sumSpans = trans.contents[0].find_all("span")
						sumTxt = ""
	
						for span in sumSpans:
							sumTxt += span.text
	
						printIndent(1, sumTxt + "\n")
						
						transDiv = trans.contents[1].contents[0]
						neoDictTrans = transDiv.find("a", 
							class_="neodictTranslation--C2TP2").text
						printIndent(2, neoDictTrans + "\n")	
						exSentence = transDiv.find("div", 
							class_="indent--FyTYr").contents[0].text
						printIndent(3, exSentence + "\n")
	
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

spanScrape(word, verbose)
