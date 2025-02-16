from tqdm import tqdm
from .utils import list_all_files
import pandas as pd
import csv


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
        efd_D100 = pd.DataFrame(columns=EFD_LAYOUT["D100"][0])
        efd_D190 = pd.DataFrame(columns=EFD_LAYOUT["D100"][0][:11] + ["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["D190"][0])
        efd_E100 = pd.DataFrame(columns=EFD_LAYOUT["E100"][0] + EFD_LAYOUT["E110"][0])
        efd_E111 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["E111"][0])
        efd_E116 = pd.DataFrame(columns=EFD_LAYOUT["E100"][0] + EFD_LAYOUT["E116"][0])
        efd_E200 = pd.DataFrame(columns=EFD_LAYOUT["E200"][0] + EFD_LAYOUT["E210"][0])
        efd_E250 = pd.DataFrame(columns=EFD_LAYOUT["E200"][0] + EFD_LAYOUT["E250"][0])
        efd_1900 = pd.DataFrame(columns=EFD_LAYOUT["1900"][0] + EFD_LAYOUT["1910"][0] + EFD_LAYOUT["1920"][0])
        efd_1921 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["1921"][0])
        efd_1926 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_LAYOUT["1926"][0])

        self._data = { "0000" : efd_0000,
                           "0150" : efd_0150,
                           "0200" : efd_0200, 
                           "C100" : efd_C100,
                           "C170" : efd_C170,
                           "C190" : efd_C190,
                           "D100" : efd_D100,
                           "D190" : efd_D190,
                           "E100" : efd_E100,
                           "E111" : efd_E111,
                           "E116" : efd_E116,
                           "E200" : efd_E200,
                           "E250" : efd_E250,
                           "1900" : efd_1900,
                           "1921" : efd_1921,
                           "1926" : efd_1926}

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self._data

    def read_from_path(self, path, file_ext = ".txt"):
        efd_files = list_all_files(path, file_ext)
        return self.read_files(efd_files)
       
    def read_files(self, files:list[str]):

        print("--- Início processamento ---")
        print("Total de arquivos encontrados a serem processados: {}" .format(len(files)))
    
        for file in tqdm(files, total=len(files), desc="Processando arquivos"): 
            self._read_efd_file(file)        

        print("--- Fim processamento ---")

        return self._data

    def _read_efd_file(self, efd_file, encoding="utf-8"):
        try:
            linha = 1
            dt_inicio = ""
            dt_fim = ""
            row_C100 = []
            row_D100 = []                        
            row_E100 = []
            row_E200 = []
            row_1900 = []
            row_1910 = []
            
            with open(efd_file, 'rt', encoding=self.encoding) as csvfile:
                leitor_csv = csv.reader(csvfile, delimiter='|')
                total_lines = sum(1 for _ in efd_file)

                for row in tqdm(leitor_csv, desc="Lendo registros", total=total_lines, unit="linhas"):
                    if row[1] == "0000":
                        self._data["0000"].loc[len(self._data["0000"])] = row[1:-1]
                        
                        # Data da escrituracao
                        dt_inicio = row[4]
                        dt_fim = row[5]

                    elif row[1] == "0150":
                        row = row[1:-1]
                        row.append(dt_inicio)
                        row.append(dt_fim)
                        self._data["0150"].loc[len(self._data["0150"])] = row
                    elif row[1] == "0200":
                        row = row[1:-1]
                        row.append(dt_inicio)
                        row.append(dt_fim)
                        self._data["0200"].loc[len(self._data["0200"])] = row
                    elif row[1] == "C100":
                        row_C100 = row[1:-1]
                        row_C100.append(dt_inicio)
                        row_C100.append(dt_fim)                               
                        self._data["C100"].loc[len(self._data["C100"])] =  row_C100
                    elif row[1] == "C170":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["C170"].loc[len(self._data["C170"])] =  row 
                    elif row[1] == "C190":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["C190"].loc[len(self._data["C190"])] =  row 
                    elif row[1] == "D100":
                        row_D100 = row[1:-1]
                        row_D100.append(dt_inicio)
                        row_D100.append(dt_fim)                               
                        self._data["D100"].loc[len(self._data["D100"])] =  row_D100
                    elif row[1] == "D190":
                        head = row_D100[:11] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["D190"].loc[len(self._data["D190"])] =  row
                    elif row[1] == "E100":
                        row_E100 = row[1:-1] 
                    elif row[1] == "E110":
                        row = row_E100 + row[1:-1]                          
                        self._data["E100"].loc[len(self._data["E100"])] =  row  
                    elif row[1] == "E111":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["E111"].loc[len(self._data["E111"])] =  row 
                    elif row[1] == "E116":  
                        row = row_E100 + row[1:-1]
                        self._data["E116"].loc[len(self._data["E116"])] =  row      
                    elif row[1] == "E200":
                        row_E200 = row[1:-1] 
                    elif row[1] == "E210":
                        row = row_E200 + row[1:-1]                          
                        self._data["E200"].loc[len(self._data["E200"])] =  row  
                    elif row[1] == "E250":
                        row = row_E200 + row[1:-1] 
                        self._data["E250"].loc[len(self._data["E250"])] =  row 
                    elif row[1] == "1900":
                        row_1900 = row[1:-1] 
                    elif row[1] == "1910":
                        row_1910 = row[1:-1] 
                    elif row[1] == "1920":
                        row = row_1900 + row_1910 + row[1:-1]
                        self._data["1900"].loc[len(self._data["1900"])] =  row 
                    elif row[1] == "1921": 
                        # TODO A DATA DE INICIO PODE SER DIFERENTE NA SUB-APURACAO  
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["1921"].loc[len(self._data["1921"])] =  row 
                    elif row[1] == "1926":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self._data["1926"].loc[len(self._data["1926"])] =  row 
                    linha += 1
        except FileNotFoundError as error:
            raise RuntimeError(error)
        except Exception as e:
            raise RuntimeError(f"Erro ao processar linha {linha}: {e}")
            
    