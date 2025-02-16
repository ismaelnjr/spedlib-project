from datetime import datetime
from spedlib.nfe_reader import NFEReader
import os


class NFeExport:
    
    def __init__(self, nfe_reader: NFEReader) -> None:
        self.nfe_reader = nfe_reader

    def to_excel(self, filename):
        
        try:           
            nfe_data = self.nfe_reader.data            
            print(f"Exportando dados para o arquivo excel:{filename}")
            if not nfe_data.empty:
                 nfe_data.to_excel(filename, index=False)
            print("Concluído!")

        except Exception as e:
            raise RuntimeError(f"Erro não esperado: {e}")
    