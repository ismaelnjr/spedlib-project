from spedlib.efd_reader import EFDReader, EFD_LAYOUT
from datetime import datetime

import pandas as pd
import os


class EFDExport(object):
    
    def __init__(self, efd_reader: EFDReader) -> None:
        self.efd_reader = efd_reader
                
    def export(self, input_dir, output_dir):
    
        try:
            dt = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(output_dir, f"efd_export_{dt}.xlsx")
            print(f"Exportando dados para o arquivo excel:{filename}")
            self.to_excel(filename) 
            print("Concluído!")

        except FileNotFoundError:
            print(f"Arquivo '{input_dir}' não encontrado.")
        except Exception as e:
            print(f"Erro não esperado: {e}")            

    def to_excel(self, filename, registros = ["__all__"]) -> None:
        try:
            with pd.ExcelWriter(filename) as writer:                
                efd_data = self.efd_reader.data
                for registro in efd_data.keys():
                    if registro in registros or "__all__" in registros:
                        sheet_name = EFD_LAYOUT[registro][1]
                        efd_data[registro].to_excel(writer, index=False, sheet_name=sheet_name)
        except Exception as e:
            raise RuntimeError(f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {e}")
  