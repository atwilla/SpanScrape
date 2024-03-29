#!/bin/bash

echo "Beginning tests..."
echo "Testing English to Spanish..."
echo

readarray EN_WORDS < testwords-en.txt

for WORD in ${EN_WORDS[@]}; do
	echo $WORD
	python3 spanscrape.py $WORD
	echo 
done

echo "Testing Spanish to English...\n"
echo

readarray ES_WORDS < testwords-es.txt

for WORD in ${ES_WORDS[@]}; do
	echo $WORD
	python3 spanscrape.py $WORD
	echo
done

echo "Done testing!"
