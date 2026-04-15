from tqdm import tqdm
from .utils import list_all_files
import pandas as pd
import os
import time


# Registros do EFD/ICMS e respectivas colunas
EFD_LAYOUT = { 
            "0000" : [["0000",
                      "COD_VER",
                      "COD_FIN",
                      "DT_INI",
                      "DT_FIN",
                      "NOME",
                      "CNPJ",
                      "CPF",
                      "UF",
                      "IE",
                      "COD_MUN",
                      "IM",
                      "SUFRAMA",
                      "IND_PERFIL",
                      "IND_ATIV"], "0000 - ABERTURA"],
        
            "0150" : [["0150",
                      "COD_PART",
                      "NOME",
                      "COD_PAIS",
                      "CNPJ",
                      "CPF",
                      "IE",
                      "COD_MUN",
                      "SUFRAMA",
                      "END",
                      "NUM",
                      "COMPL",
                      "BAIRRO",
                      "_DT_INI",
                      "_DT_FIN"], "0150 - PARTICIPANTES"],

           "0200" : [["0200",
                     "COD_ITEM",
                     "DESCR_ITEM",
                     "COD_BARRA",
                     "COD_ANT_ITEM",
                     "UNID_INV",
                     "TIPO_ITEM",
                     "COD_NCM",
                     "EX_IPI",
                     "COD_GEN",
                     "COD_LST",
                     "ALIQ_ICMS",
                     "CEST",
                     "_DT_INI",
                     "_DT_FIN"], "0200 - PRODUTOS"],

           "C100" : [["C100",
                     "IND_OPER",
                     "IND_EMIT",
                     "COD_PART",
                     "COD_MOD",
                     "COD_SIT",
                     "SER",
                     "NUM_DOC",
                     "CHV_NFE",
                     "DT_DOC",
                     "DT_E_S",
                     "VL_DOC",
                     "IND_PGTO",
                     "VL_DESC",
                     "VL_ABAT_NT",
                     "VL_MERC",
                     "IND_FRT",
                     "VL_FRT",
                     "VL_SEG",
                     "VL_OUT_DA",
                     "VL_BC_ICMS",
                     "VL_ICMS",
                     "VL_BC_ICMS_ST",
                     "VL_ICMS_ST",
                     "VL_IPI", 
                     "VL_PIS",
                     "VL_COFINS",
                     "VL_PIS_ST",
                     "VL_COFINS_ST",
                     "_DT_INI",
                     "_DT_FIN"], "C100 - DOCUMENTOS"],
                     
            "C170": [["C170",
                     "NUM_ITEM",
                     "COD_ITEM",
                     "DESCR_COMPL",
                     "QTD","UNID",
                     "VL_ITEM",
                     "VL_DESC",
                     "IND_MOV",
                     "CST_ICMS",
                     "CFOP",
                     "COD_NAT",
                     "VL_BC_ICMS",
                     "ALIQ_ICMS",
                     "VL_ICMS",
                     "VL_BC_ICMS_ST",
                     "ALIQ_ST",
                     "VL_ICMS_ST",
                     "IND_APUR",
                     "CST_IPI",
                     "COD_ENQ",
                     "VL_BC_IPI",
                     "ALIQ_IPI",
                     "VL_IPI",
                     "CST_PIS",
                     "VL_BC_PIS",
                     "ALIQ_PIS",
                     "QUANT_BC_PIS",
                     "ALIQ_PIS_R",
                     "VL_PIS",
                     "CST_COFINS",
                     "VL_BC_COFINS",
                     "ALIQ_COFINS",
                     "QUANT_BC_COFINS",
                     "ALIQ_COFINS_R",
                     "VL_COFINS",
                     "COD_CTA",
                     "VL_ABAT_NT"], "C170 - ITENS DO DOCUMENTO"],  

            "C190": [["C190",
                     "CST_ICMS",
                     "CFOP",
                     "ALIQ_ICMS",
                     "VL_OPR",
                     "VL_BC_ICMS",
                     "VL_ICMS",
                     "VL_BC_ICMS_ST",
                     "VL_ICMS_ST",
                     "VL_RED_BC",
                     "VL_IPI",
                     "COD_OBS"], "C190 - TOTALIZADORES"],
            
            "C195": [["C195",
                     "COD_OBS",
                     "TXT_COMPL"], "C195 - OBS LANÇ FISCAL"],
            
            "C197": [["C197",
                     "COD_AJ",
                     "DESCR_COMPL_AJ",
                     "COD_ITEM",
                     "VL_BC_ICMS",
                     "ALIQ_ICMS",
                     "VL_ICMS",
                     "VL_OUTROS"], "C197 - AJUSTE DOC FISCAL"],
            
            "D100": [["D100",
                     "IND_OPER",
                     "IND_EMIT",
                     "COD_PART",    
                     "COD_MOD",
                     "COD_SIT",
                     "SER",
                     "SUB",
                     "NUM_DOC",
                     "CHV_NFE",
                     "DT_DOC",
                     "DT_A_P",
                     "TP_CTE",
                     "CHV_CTE_REF",
                     "VL_DOC",
                     "VL_DESC",
                     "IND_FRT",
                     "VL_SERV",
                     "VL_BC_ICMS",
                     "VL_ICMS",
                     "VL_NT",
                     "COD_INF",
                     "COD_CTA",
                     "COD_MUN_ORIG",
                     "COD_MUN_DEST",
                     "_DT_INI",
                     "_DT_FIN"], "D100 - TRANSPORTE"],
            
            "D190": [["D190",
                     "CST_ICMS",
                     "CFOP",
                     "ALIQ_ICMS",
                     "VL_OPR",
                     "VL_BC_ICMS",
                     "VL_ICMS",
                     "VL_RED_BC",
                     "COD_OBS"], "D190 - TRANSP. TOTAL"],

            "E100": [["E100",
                     "DT_INI_APUR",
                     "DT_FIN_APUR"], "E100 - PERIODO ICMS"],

            "E110": [["E110",
                     "VL_TOT_DEBITOS",
                     "VL_AJ_DEBITOS",
                     "VL_TOT_AJ_DEBITOS",
                     "VL_ESTORNOS_CRED",
                     "VL_TOT_CREDITOS",
                     "VL_AJ_CREDITOS",
                     "VL_TOT_AJ_CREDITOS",
                     "VL_ESTORNOS_DEB",
                     "VL_SLD_CREDOR_ANT",
                     "VL_SD_APURADO",
                     "VL_TOT_DED",
                     "VL_ICMS_RECOLHER",
                     "VL_SLD_CREDOR_TRANSPORTAR",
                     "DEB_ESP"], "E110 - APURACAO ICMS"],  

            "E111": [["E111",
                     "COD_AJ_APUR",
                     "DESCR_COMPL_AJ",
                     "VL_AJ_APUR"], "E111 - AJUSTES ICMS"],                              
                     
            "E116": [["E116",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"], "E116 - OBRIG ICMS"],
            
            "E200": [["E200",
                     "UF",
                     "DT_INI_APUR",
                     "DT_FIN_APUR"], "E200 - PERIODO ICMS-ST"],
            
            "E210": [["E210",
                     "IND_MOV_ST",
                     "VL_SLD_CRED_ANT_ST",
                     "VL_DEVOL_ST",
                     "VL_RESSARC_ST",
                     "VL_OUT_CRED_ST",
                     "VL_AJ_CREDITOS_ST",
                     "VL_RETENCAO_ST",
                     "VL_OUT_DEB_ST",
                     "VL_AJ_DEBITOS_ST",
                     "VL_SLD_DEV_ANT_ST",
                     "VL_DEDUCOES_ST",
                     "VL_ICMS_RECOL_ST",
                     "VL_SLD_CRED_ST_TRANSPORTAR",
                     "DEB_ESP_ST"], "E210 - APURACAO ICMS-ST"],

            "E250": [["E250",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"], "E250 - OBRIG ICMS-ST"],
            
            "H005": [["H005",
                     "DT_INV",
                     "VL_INV",
                     "MOT_INV"], "H005 - TOTAIS INVENTARIO"],
            
            "H010": [["H010",
                     "COD_ITEM",
                     "UNID",
                     "QTD",
                     "VL_UNIT",
                     "VL_ITEM",
                     "IND_PROP",
                     "COD_PART",
                     "TXT_COMPL",
                     "COD_CTA",
                     "VL_ITEM_IR",
                     "_DT_INI",
                     "_DT_FIN",], "H010 - INVENTARIO"],
            
            "H020": [["H020",
                     "CST_ICMS",
                     "BC_ICMS",
                     "VL_ICMS",
                     "_DT_INI",
                     "_DT_FIN",], "H020 - INF COMPL INV"],

            "1900": [["1900",
                     "IND_APUR_ICMS",
                     "DESCR_COMPL_OUT_APUR"], "1900 - SUB-APURACAO"],
                     
            "1910": [["1910",
                     "DT_INI",
                     "DT_FIN"], "1910 - PERIODO SUB-APURACAO"],

            "1920": [["1920",
                     "VL_TOT_TRANSF_DEBITOS_OA",
                     "VL_TOT_AJ_DEBITOS_OA",
                     "VL_ESTORNOS_CRED_OA",
                     "VL_TOT_TRANSF_CREDITOS_OA",
                     "VL_TOT_AJ_CREDITOS_OA",
                     "VL_ESTORNOS_DEB_OA",
                     "VL_SLD_CREDOR_ANT_OA",
                     "VLSLD_APURADO_OA",
                     "VL_TOT_DED",
                     "VL_ICMS_RECOLHER_OA",
                     "VL_SLD_CREDOR_TRANSP_OA",
                     "DEB_ESP_OA"], "1920 - TOTAL SUB-APURACAO"],
                     
            "1921": [["1921",
                     "COD_AJ_APUR",
                     "DESCR_COMPL_AJ",
                     "VL_AJ_APUR"], "1921 - AJUSTES SUB-APURACAO"],
                     
            "1926": [["1926",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"], "1926 - OBRIG SUB-APURACAO"],
            }


# Classe para leitura do sped ICMS/IPI
class EFDReader():

    _data = {}

    def __init__(self, encoding="utf-8") -> None:
        pd.options.display.float_format = "{:,.2f}".format
        self.encoding = encoding        
        
        efd_0000 = pd.DataFrame(columns=EFD_LAYOUT["0000"][0])
        efd_0150 = pd.DataFrame(columns=EFD_LAYOUT["0150"][0])
        efd_0200 = pd.DataFrame(columns=EFD_LAYOUT["0200"][0])
        efd_C100 = pd.DataFrame(columns=EFD_LAYOUT["C100"][0])
        efd_C170 = pd.DataFrame(columns=EFD_LAYOUT["C100"][0][:8] + ["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["C170"][0])
        efd_C190 = pd.DataFrame(columns=EFD_LAYOUT["C100"][0][:8] + ["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["C190"][0])
        efd_C197 = pd.DataFrame(columns=EFD_LAYOUT["C100"][0][:8] + ["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["C195"][0] + EFD_LAYOUT["C197"][0])
        efd_D100 = pd.DataFrame(columns=EFD_LAYOUT["D100"][0])
        efd_D190 = pd.DataFrame(columns=EFD_LAYOUT["D100"][0][:11] + ["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["D190"][0])
        efd_E100 = pd.DataFrame(columns=EFD_LAYOUT["E100"][0] + EFD_LAYOUT["E110"][0])
        efd_E111 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["E111"][0])
        efd_E116 = pd.DataFrame(columns=EFD_LAYOUT["E100"][0] + EFD_LAYOUT["E116"][0])
        efd_E200 = pd.DataFrame(columns=EFD_LAYOUT["E200"][0] + EFD_LAYOUT["E210"][0])
        efd_E250 = pd.DataFrame(columns=EFD_LAYOUT["E200"][0] + EFD_LAYOUT["E250"][0])
        efd_H005 = pd.DataFrame(columns=EFD_LAYOUT["H005"][0])
        efd_H010 = pd.DataFrame(columns=EFD_LAYOUT["H010"][0])
        efd_1900 = pd.DataFrame(columns=EFD_LAYOUT["1900"][0] + EFD_LAYOUT["1910"][0] + EFD_LAYOUT["1920"][0])
        efd_1921 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["1921"][0])
        efd_1926 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["1926"][0])

        self._data = { "0000" : efd_0000,
                           "0150" : efd_0150,
                           "0200" : efd_0200, 
                           "C100" : efd_C100,
                           "C170" : efd_C170,
                           "C190" : efd_C190,
                           "C197" : efd_C197,
                           "D100" : efd_D100,
                           "D190" : efd_D190,
                           "E100" : efd_E100,
                           "E111" : efd_E111,
                           "E116" : efd_E116,
                           "E200" : efd_E200,
                           "E250" : efd_E250,
                           "H005" : efd_H005,
                           "H010" : efd_H010,
                           "1900" : efd_1900,
                           "1921" : efd_1921,
                           "1926" : efd_1926}

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self._data

    def is_empty(self) -> bool:
        return self._data["0000"].empty

    def read_from_path(self, path, file_ext = ".txt"):
        efd_files = list_all_files(path, file_ext)
        return self.read_files(efd_files)
       
    def read_files(self, files:list[str]):

        print("--- Início processamento ---")
        print("Total de arquivos encontrados a serem processados: {}" .format(len(files)))
    
        for file in tqdm(files, total=len(files), desc="Processando arquivos"): 
            self.read_file(file)        

        print("--- Fim processamento ---")

        return self._data

    def _flush_buffers(self, buffers: dict[str, list[list[str]]]) -> None:
        for registro, rows in buffers.items():
            if not rows:
                continue

            chunk_df = pd.DataFrame.from_records(rows, columns=self._data[registro].columns)
            if self._data[registro].empty:
                self._data[registro] = chunk_df
            else:
                self._data[registro] = pd.concat(
                    [self._data[registro], chunk_df],
                    ignore_index=True,
                )

    def read_file(self, filename: str, progress_callback=None, progress_interval: int = 5000):
        try:
            linha = 1
            dt_inicio = ""
            dt_fim = ""
            row_C100 = []
            row_C195 = []
            row_D100 = []                        
            row_E100 = []
            row_E200 = []
            row_1900 = []
            row_1910 = []
            start_time = time.time()
            bytes_total = os.path.getsize(filename)
            lines_processed = 0
            bytes_processed = 0
            last_notified_at = start_time
            min_notify_interval = 0.5
            buffers = {registro: [] for registro in self._data}

            def _notify_progress(processed_lines: int, force: bool = False):
                nonlocal last_notified_at
                if not progress_callback:
                    return
                now = time.time()
                if not force and (now - last_notified_at < min_notify_interval):
                    return

                last_notified_at = now

                elapsed_seconds = max(now - start_time, 0.0)
                percent = (bytes_processed / bytes_total * 100) if bytes_total else 100.0
                bytes_rate = (bytes_processed / elapsed_seconds) if elapsed_seconds > 0 else 0.0
                remaining_bytes = max(bytes_total - bytes_processed, 0)
                eta_seconds = (remaining_bytes / bytes_rate) if bytes_rate > 0 else 0.0

                progress_callback(
                    processed_lines=processed_lines,
                    total_lines=None,
                    percent=percent,
                    elapsed_seconds=elapsed_seconds,
                    eta_seconds=eta_seconds,
                )

            with open(filename, 'rt', encoding=self.encoding) as csvfile:
                for linha, raw_line in enumerate(tqdm(csvfile, desc="Lendo registros", unit="linhas"), start=1):
                    row = raw_line.rstrip("\r\n").split("|")
                    if len(row) < 3:
                        continue

                    registro = row[1]
                    row_data = row[1:-1]

                    if registro == "0000":
                        buffers["0000"].append(row_data)
                        
                        # Data da escrituracao
                        dt_inicio = row[4]
                        dt_fim = row[5]

                    elif registro == "0150":
                        row_data.append(dt_inicio)
                        row_data.append(dt_fim)
                        buffers["0150"].append(row_data)
                    elif registro == "0200":
                        row_data.append(dt_inicio)
                        row_data.append(dt_fim)
                        buffers["0200"].append(row_data)
                    elif registro == "C100":
                        row_C100 = row_data
                        row_C100.append(dt_inicio)
                        row_C100.append(dt_fim)                               
                        buffers["C100"].append(row_C100)
                    elif registro == "C170":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["C170"].append(head + row_data)
                    elif registro == "C190":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["C190"].append(head + row_data)
                    elif registro == "C195":
                        row_C195 = row_data
                    elif registro == "C197":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["C197"].append(head + row_C195 + row_data)
                    elif registro == "D100":
                        row_D100 = row_data
                        row_D100.append(dt_inicio)
                        row_D100.append(dt_fim)                               
                        buffers["D100"].append(row_D100)
                    elif registro == "D190":
                        head = row_D100[:11] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["D190"].append(head + row_data)
                    elif registro == "E100":
                        row_E100 = row_data
                    elif registro == "E110":
                        buffers["E100"].append(row_E100 + row_data)
                    elif registro == "E111":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["E111"].append(head + row_data)
                    elif registro == "E116":
                        buffers["E116"].append(row_E100 + row_data)
                    elif registro == "E200":
                        row_E200 = row_data
                    elif registro == "E210":
                        buffers["E200"].append(row_E200 + row_data)
                    elif registro == "E250":
                        buffers["E250"].append(row_E200 + row_data)
                    elif registro == "H005":
                        buffers["H005"].append(row_data)
                    elif registro == "H010":
                        row_data.append(dt_inicio)
                        row_data.append(dt_fim)
                        buffers["H010"].append(row_data)
                    elif registro == "1900":
                        row_1900 = row_data
                    elif registro == "1910":
                        row_1910 = row_data
                    elif registro == "1920":
                        buffers["1900"].append(row_1900 + row_1910 + row_data)
                    elif registro == "1921": 
                        # TODO A DATA DE INICIO PODE SER DIFERENTE NA SUB-APURACAO  
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["1921"].append(head + row_data)
                    elif registro == "1926":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        buffers["1926"].append(head + row_data)

                    lines_processed = linha
                    bytes_processed += len(raw_line)
                    if linha % progress_interval == 0:
                        _notify_progress(linha)

                bytes_processed = bytes_total
                if lines_processed == 0:
                    _notify_progress(0, force=True)
                else:
                    _notify_progress(lines_processed, force=True)

            self._flush_buffers(buffers)
        except FileNotFoundError as error:
            raise RuntimeError(error)
        except Exception as e:
            raise RuntimeError(f"Erro ao processar linha {linha}: {e}")
            
    