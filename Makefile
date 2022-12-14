run: 
	python3 ./project-code/sentimentAnalysis.py

setup: requirements.txt
	pip install -r requirements.txt

clean: 
	rm -rf ./project-code/__pycache__
view-result:
	cat ./project-code/Sentiment_Scores.csv
	