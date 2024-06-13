import pandas as pd
import apache_beam as beam


class CSVToDictGenerator(beam.DoFn):
    def __init__(self, file_path):
        """
        Classe que lê um arquivo CSV e fornece um generator que produz dicionários
        representando as linhas do CSV.

        Args:
        file_path (str): O caminho do arquivo CSV.
        """
        self.file_path = file_path

    def process(self, element):
        try:
            dataframe = pd.read_csv(self.file_path)
            
            for record in dataframe.to_dict(orient='records'):
                print(record)
                yield record
                
        except FileNotFoundError:
            print("Arquivo não encontrado.")
        except Exception as e:
            print("Ocorreu um erro:", e)
