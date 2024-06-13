from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions
from beam_data.options.p_options import Config_Options
from beam_data.io.csv_to_dict import CSVToDictGenerator
from beam_data.utils.getting_sm import access_secret_version

import apache_beam as beam
from pathlib import Path
import logging
import json
import os


def main(argv=None):
    pipeline_options = PipelineOptions()
    pipe_options = pipeline_options.view_as(Config_Options)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pip_dict = pipeline_options.get_all_options()


    credentials_json = access_secret_version(project_id='lima-consulting-prd', secret_id='sm-limaconsulting')
    
    # Escrever as credenciais em um arquivo temporário
    temp_credentials_path = '/tmp/google_application_credentials.json'
    with open(temp_credentials_path, 'w') as f:
        json.dump(credentials_json, f)  # Escreve a string JSON no arquivo


    FILE_PATH = Path(__file__).parent / 'beam_data' / 'schemas' / 'NEWS.json'

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_credentials_path
    schema_bq = None


    with open(FILE_PATH, 'r') as file:
        schema_bq = json.loads(file.read())

    with beam.Pipeline(options=pipeline_options) as p:

        conection_bd = (
            p
            | "START" >> beam.Create(['START'])
            | "CSV_To_Dict" >> beam.ParDo(CSVToDictGenerator('/home/fernando/repositorios/news-scraper-bigquery/news_scraper/news.csv'))
        )

        carga = (
        conection_bd
        | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
            table=f'lima-consulting-prd:BBC.NEWS',
            project='lima-consulting-prd',
            schema=schema_bq,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            additional_bq_parameters={
                            'ignoreUnknownValues': True,
                        }
            )
        )    


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()