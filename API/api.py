from fastapi import FastAPI, Query
from google.cloud import bigquery
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.openapi.docs import get_redoc_html

app = FastAPI()

client = bigquery.Client()

# Endpoint raiz com redirecionamento para documentação
@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/docs")

@app.get("/extract-data", response_model=dict)
async def extract_data(project: str = Query(..., description="ID do projeto BigQuery"),
                       dataset: str = Query(..., description="Nome do dataset"),
                       table: str = Query(..., description="Nome da tabela")):
    """
    Endpoint para extrair tabela do Bigquery.

    Parâmetros:
    - project: ID do projeto BigQuery.
    - dataset: Nome do dataset.
    - table: Nome da tabela.

    Exemplo de Requisição:
    GET /extract-data?project=meu-projeto&dataset=meu-dataset&table=minha-tabela

    Exemplo de Resposta:
    {
        "results": [
            {"coluna1": "valor1", "coluna2": "valor2"},
            {"coluna1": "valor3", "coluna2": "valor4"}
        ]
    }

    """
    try:
        query = f"SELECT * FROM `{project}.{dataset}.{table}`"
        query_job = client.query(query)

        results = []
        for row in query_job:
            results.append(dict(row))

        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

# Endpoint para buscar palavras dentro de uma tabela do BigQuery
@app.get("/search", response_model=dict)
async def search_data(project: str = Query(..., description="ID do projeto BigQuery"),
                      dataset: str = Query(..., description="Nome do dataset"),
                      table: str = Query(..., description="Nome da tabela"),
                      column: str = Query(..., description="Nome da coluna para buscar"),
                      search_term: str = Query(..., description="Termo de busca")):
    """
    Endpoint para buscar palavras dentro de uma tabela do BigQuery.

    Retornará a linha com o registro que contém a string de busca.

    Parâmetros:
    - project: ID do projeto BigQuery.
    - dataset: Nome do dataset.
    - table: Nome da tabela.
    - column: Nome da coluna para buscar.
    - search_term: Termo de busca.
    
    Exemplo de Requisição:
    GET /extract-data?project=meu-projeto&dataset=meu-dataset&table=minha-tabela

    Exemplo de Resposta:
    {
        "results": [
            {"coluna1": "valor1", "coluna2": "valor2"},
            {"coluna1": "valor3", "coluna2": "valor4"}
        ]
    }

    """
    try:
        query = f"""
        SELECT * FROM `{project}.{dataset}.{table}`
        WHERE {column} LIKE '%{search_term}%'
        LIMIT 10
        """
        query_job = client.query(query)

        results = []
        for row in query_job:
            results.append(dict(row))

        return {"results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})