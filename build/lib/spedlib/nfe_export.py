from datetime import datetime
from spedlib.nfe_reader import NFEReader
import os


class NFeExport:
    
    def __init__(self, nfe_reader: NFEReader) -> None:
        self.nfe_reader = nfe_reader

    def export(self, input_dir, output_dir):
        
        try:
            dt = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(output_dir, f"nfe_export_{dt}.xlsx")
            nfe_data = self.nfe_reader.data
            
            print(f"Exportando dados para o arquivo excel:{filename}")
            if not nfe_data.empty:
                 nfe_data.to_excel(filename, index=False)
            print("Concluído!")

        except FileNotFoundError:
            raise RuntimeError(f"Arquivo '{input_dir}' não encontrado.")

        except Exception as e:
            raise RuntimeError(f"Erro não esperado: {e}")
    