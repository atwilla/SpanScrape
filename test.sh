#!/bin/bash

echo "Beginning tests..."
echo "Testing English to Spanish..."

readarray EN_WORDS < testwords-en.txt
NUM_WORDS=${#EN_WORDS[@]}

for WORD in ${EN_WORDS[@]}; do
	echo $WORD
	python3 spanscrape.py $WORD
done
