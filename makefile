install:
	pip install -r requirements.txt

build:
	gcloud builds submit . --

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

scrapy_bbc:
	bash -c "source venv/bin/activate && cd news_scraper && scrapy crawl bbc -O news.csv"