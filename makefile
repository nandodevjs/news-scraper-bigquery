install:
	pip install -r requirements.txt


scrapy_bbc:
	bash -c "cd news_scraper && scrapy crawl bbc -O news.csv"


run:
	python3 main.py \
	--runner DirectRunner \
	--max-workers 5 \
	--project lima-consulting-prd \
	--job_name pipeline-started-`date +%Y%m%d-%H%M%S` \
	--region southamerica-east1 \
	--temp_location gs://scrapy-bbc/Dataflow/temp \
	--staging_location gs://scrapy-bbc/Dataflow/staging \
	--setup_file ./setup.py \

api_local:
	bash -c "cd API && uvicorn api:app --reload"


build:
	gcloud builds submit . --