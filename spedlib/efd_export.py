from spedlib.efd_reader import EFDReader, EFD_LAYOUT
from datetime import datetime

import pandas as pd
import os
import time


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

    def _get_exportable_records(self, registros=None) -> list[str]:
        efd_data = self.efd_reader.data
        if registros is None or "__all__" in registros:
            candidatos = list(efd_data.keys())
        else:
            candidatos = [registro for registro in registros if registro in efd_data]

        return [registro for registro in candidatos if not efd_data[registro].empty]

    def to_excel(self, filename, registros=None) -> None:
        try:
            efd_data = self.efd_reader.data
            export_records = self._get_exportable_records(registros)
            if not export_records:
                raise RuntimeError("Nenhum registro com dados para exportar.")

            started_at = time.perf_counter()
            total_rows = 0
            with pd.ExcelWriter(
                filename,
                engine="xlsxwriter",
                engine_kwargs={"options": {"strings_to_urls": False}},
            ) as writer:
                for registro in export_records:
                    sheet_name = EFD_LAYOUT[registro][1]
                    df = efd_data[registro]
                    total_rows += len(df)
                    df.to_excel(writer, index=False, sheet_name=sheet_name)

            elapsed_seconds = time.perf_counter() - started_at
            print(
                "Exportacao Excel concluida em "
                f"{elapsed_seconds:.2f}s - {len(export_records)} abas e {total_rows} linhas."
            )
        except Exception as e:
            raise RuntimeError(f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {e}")
  