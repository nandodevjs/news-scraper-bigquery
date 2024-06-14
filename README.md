# Projeto de Extração de Dados do BigQuery com Scrapy, Apache Beam e FastAPI

Este projeto é uma aplicação composta por três componentes principais: um scraper desenvolvido com Scrapy, um pipeline de processamento de dados com Python e Apache Beam, e uma API construída com FastAPI para extração e consulta de dados armazenados no BigQuery.

## Sumário

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Configuração e Instalação](#configuração-e-instalação)
- [Execução do ETL](#Execução-do-projeto)


# Estrutura do Projeto
├── API
│ ├── api.py
│ ├── cloudbuild.yaml
│ ├── Dockerfile
│ └── requirements.txt
├── beam_data
│ ├── io
│ │ └── init.py
│ │ └── csv_to_dict.py
│ ├── options
│ │ └── p_options.py
│ ├── schemas
│ │ └── NEWS.json
│ ├── utils
│ │ └── getting_sm.py
├── news_scraper
│ ├── news_scraper
│ │ ├── spiders
│ │ │ ├── init.py
│ │ │ └── bbc.py
│ │ ├── init.py
│ │ ├── items.py
│ │ ├── middlewares.py
│ │ ├── pipelines.py
│ │ ├── settings.py
│ ├── .dockerignore
│ ├── Dockerfile
│ ├── news.csv
│ ├── requirements.txt
│ ├── scrapy.cfg
│ └── urls.txt
├── venv (Ambiente Virtual Python)
├── .dockerignore
├── .gitignore
├── cloudbuild.yaml
├── Dockerfile
├── main.py
├── makefile
├── metadata.json
├── README.md
├── requirements.txt
└── setup.py

## Pré-requisitos
Conta no Google Cloud Platform (GCP)
Google Cloud SDK
Docker
Terraform

# Configuração e Instalação
## 1. Clonar o Repositório
git clone git@github.com:nandodevjs/news-scraper-bigquery.git

## 2. Instalar Dependências
sudo apt-get update
sudo apt-get install make

## Execução do projeto
Iremos utilizar comandos no nosso terminal para executar o projeto, tudo está configurado no arquivo makefile.

O primeiro comando que iremos executar é o seguinte:

make install:
    este comando irá instalar todas as dependencias de nosso projeto.
        (pip install -r requirements.txt)

make scrapy_bbc:
    este comando irá executar a extração de dados do site BBC.
	    bash -c "cd news_scraper && scrapy crawl bbc -O news.csv"

make run:
    este comando irá processar os dados e fazer a carga dos dados no Bigquery.
        python3 main.py \
        --runner DirectRunner \
        --max-workers 5 \
        --project lima-consulting-prd \
        --job_name pipeline-started-`date +%Y%m%d-%H%M%S` \
        --region southamerica-east1 \
        --temp_location gs://scrapy-bbc/Dataflow/temp \
        --staging_location gs://scrapy-bbc/Dataflow/staging \
        --setup_file ./setup.py \

make api_local:
    este comando irá disponibilizar a API localmente. (a mesma já está hospedada no cloud run, basta acessar através do link: https://api-extract-thvvwrfusa-rj.a.run.app/docs)
	    bash -c "cd API && uvicorn api:app --reload"

# API

## documentação API

## /extract-data
Este endpoint retorna todos os registros da tabela

    Parâmetros:
        - project: ID do projeto BigQuery.
        - dataset: Nome do dataset.
        - table: Nome da tabela.

        Exemplo de Requisição:
        GET /extract-data?project={meu-projeto}&dataset={meu-dataset}&table={minha-tabela}

## /search
Endpoint para buscar palavras dentro de uma tabela do BigQuery.

    Retornará a linha com o registro que contém a string de busca.

    Parâmetros:
    - project: ID do projeto BigQuery.
    - dataset: Nome do dataset.
    - table: Nome da tabela.
    - column: Nome da coluna para buscar.
    - search_term: Termo de busca.

## Valores dos Parâmetros para testar a API:

    - URL da API: https://api-extract-thvvwrfusa-rj.a.run.app/docs
    - project: lima-consulting-prd
    - dataset: BBC
    - table: NEWS.
    - column: URL, TITLE, PUBLICATION_DATE, AUTHOR, NEWS (escolha uma para realizar a busca)
    - search_term: (dica: utilize alguma URL do arquivo urls.txt e busque com a coluna NEWS)

# URLS para extração:

As URLS estão no arquivo urls.txt, caso queira adicionar uma nova URL, basta adicionar nele e setar no arquivo BBC.py dentro dos spiders.
── news_scraper
│ ├── news_scraper
│ │ ├── spiders     <-----
│ │ │ ├── init.py
│ │ │ └── bbc.py    <-----
│ │ ├── init.py
│ │ ├── items.py
│ │ ├── middlewares.py
│ │ ├── pipelines.py
│ │ ├── settings.py
│ ├── .dockerignore
│ ├── Dockerfile
│ ├── news.csv
│ ├── requirements.txt
│ ├── scrapy.cfg
│ └── urls.txt      <-----


# Resumo:

Para executar o projeto, precisa somente instalar o make, instalar as dependencias que estão nos requirements.txt, rodar os comandos de scrapy e run que estão no Makefile. Lembrando que a API está online no Cloud Run mas também é possível rodar localmente com make api_local. Qualquer dúvida, solicitar meu contato para a recrutadora Debora.