from tqdm import tqdm
from datetime import date, datetime

import os
import xml.etree.ElementTree as et
import pandas as pd
import csv


# Dicionário com os códigos dos estados
codigos_uf = {
    '11': ('RO', 'Rondônia'),
    '12': ('AC', 'Acre'),
    '13': ('AM', 'Amazonas'),
    '14': ('RR', 'Roraima'),
    '15': ('PA', 'Pará'),
    '16': ('AP', 'Amapá'),
    '17': ('TO', 'Tocantins'),
    '21': ('MA', 'Maranhão'),
    '22': ('PI', 'Piauí'),
    '23': ('CE', 'Ceará'),
    '24': ('RN', 'Rio Grande do Norte'),
    '25': ('PB', 'Paraíba'),
    '26': ('PE', 'Pernambuco'),
    '27': ('AL', 'Alagoas'),
    '28': ('SE', 'Sergipe'),
    '29': ('BA', 'Bahia'),
    '31': ('MG', 'Minas Gerais'),
    '32': ('ES', 'Espírito Santo'),
    '33': ('RJ', 'Rio de Janeiro'),
    '35': ('SP', 'São Paulo'),
    '41': ('PR', 'Paraná'),
    '42': ('SC', 'Santa Catarina'),
    '43': ('RS', 'Rio Grande do Sul'),
    '50': ('MS', 'Mato Grosso do Sul'),
    '51': ('MT', 'Mato Grosso'),
    '52': ('GO', 'Goiás'),
    '53': ('DF', 'Distrito Federal')
}

# Dicionário com colunas de uma NFe
XML_Cols = ["NUM_NFE",
            "SERIE",
            "DT_EMISSAO",
            "CHAVE_NFE",
            "TIPO_NFE",
            "CNPJ_EMIT",
            "NOME_EMIT",
            "CNPJ_DEST",
            "CPF_DEST",
            "NOME_NOME_DEST",
            "UF",
            "VALOR_NFE",
            "IDX_ITEM",
            "COD_PROD",
            "DESC_PROD",
            "NCM","CFOP",
            "UNID",
            "VLR_UNIT",
            "QTDE",
            "VLR_PROD",
            "FRETE",
            "SEGURO",
            "DESC",
            "OUTROS",
            "T_ITEM",
            "ORIGEM",
            "CST_ICMS",
            "BC_ICMS",
            "ALQ_ICMS",
            "ICMS",
            "MVA",
            "BC_ICMSST",
            "ALQ_ICMSST",
            "ICMSST",
            "CST_IPI",
            "IPI",
            "STATUS_NFE", 
            "MES_ANO",
            "DATA_IMPORTACAO"]

# Registros do EFD/ICMS e respectivas colunas
EFD_Cols = { 
            "0000" : ["0000",
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
                      "IND_ATIV"],
        
            "0150" : ["0150",
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
                      "_DT_FIN"],

           "0200" : ["0200",
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
                     "_DT_FIN"],

           "C100" : ["C100",
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
                     "_DT_FIN"], 
                     
            "C170": ["C170",
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
                     "VL_ABAT_NT"],   

            "C190": ["C190",
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
                     "COD_OBS"],
            
            "D100": ["D100",
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
                     "_DT_FIN"],
            
            "D190": ["D190",
                     "CST_ICMS",
                     "CFOP",
                     "ALIQ_ICMS",
                     "VL_OPR",
                     "VL_BC_ICMS",
                     "VL_ICMS",
                     "VL_RED_BC",
                     "COD_OBS"],

            "E100": ["E100",
                     "DT_INI_APUR",
                     "DT_FIN_APUR"],

            "E110": ["E110",
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
                     "DEB_ESP"],   

            "E111": ["E111",
                     "COD_AJ_APUR",
                     "DESCR_COMPL_AJ",
                     "VL_AJ_APUR"],                               
                     
            "E116": ["E116",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"],
            
            "E200": ["E200",
                     "UF",
                     "DT_INI_APUR",
                     "DT_FIN_APUR"],
            
            "E210": ["E210",
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
                     "DEB_ESP_ST"],

            "E250": ["E250",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"],

            "1900": ["1900",
                     "IND_APUR_ICMS",
                     "DESCR_COMPL_OUT_APUR"],
                     
            "1910": ["1910",
                     "DT_INI",
                     "DT_FIN"],

            "1920": ["1920",
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
                     "DEB_ESP_OA"],
                     
            "1921": ["1921",
                     "COD_AJ_APUR",
                     "DESCR_COMPL_AJ",
                     "VL_AJ_APUR"],
                     
            "1926": ["1926",
                     "COD_OR",
                     "VL_OR",
                     "DT_VCTO",
                     "COD_REC",
                     "NUM_PROC",
                     "IND_PROC",
                     "PROC",
                     "TXT_COMPL",
                     "MES_REF"]}

# Funções genéricas para tratamento de dados
def checkNone(var):
    if var == None:
        return ""
    else:
        try:
            return var.text.replace('.',',')
        except:
            return var.text

def checkInt(var):
    if var == None:
        return 0
    else:
        try:
            return int(var.text)
        except:
            return 0

def checkFloat(var):
    if var == None:
        return 0.0
    else:
        try:
            return float(var.text)
        except:
            return 0.0

def formatCNPJ(cnpj):
    if cnpj == "":
        return ""
    try:
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
        return cnpj
    except:
        return ""
        
def formatCPF(cpf):
    if cpf == "":
        return ""
    try:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    except:
        return ""
    
def create_doc_id(self, serie, num_doc, cod_par):
        
    #s_id = f"{num_doc:09}:{serie:03}"
    s_id = str(cod_par) + ":" + str(num_doc).zfill(9) + ":" + str(serie) 
    return s_id

# Classe abstrata para leitura de um documento fiscal
class docReader():

    def __init__(self) -> None:
        pd.options.display.float_format = "{:,.2f}".format

    def listAllFiles(self, current_dir, file_ext):

        files = []

        for f in os.listdir(current_dir):
            if f.lower().endswith(file_ext):
                files.append(os.path.join(current_dir, f))
        
        return files
        
     
# Classe para leitura de NFe (modelo 55)
class XMLReader(docReader):

    def __init__(self) -> None:
        docReader.__init__(self)

    def readXMLContent(self, xml):
        
        data = []
        rootXML = et.parse(xml).getroot()
        
        if "nfeProc" in rootXML.tag:
                 
            nsNFe = {"ns": "http://www.portalfiscal.inf.br/nfe"}

            # DADOS DA NFE        
            numNFe = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF" , nsNFe))
            serie = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFe))
            dataEmissao = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe))
            dataEmissao = F"{dataEmissao[8:10]}/{dataEmissao[5:7]}/{dataEmissao[:4]}"
            if checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpNF", nsNFe)) == 0:
                tpNF = "ENTRADA"
            else:
                tpNF = "SAIDA"
            
            mesAno = F"{dataEmissao[-4:]}_{dataEmissao[3:5]}"
            
            chave = checkNone(rootXML.find("./ns:protNFe/ns:infProt/ns:chNFe", nsNFe))
            cnpjEmit = formatCNPJ (checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ", nsNFe)))
            nomeEmit = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:emit/ns:xNome", nsNFe))
            
            cnpjDest = formatCNPJ(checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ", nsNFe)))
            cpfDest = formatCPF (checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:CPF", nsNFe)))
            nomeDest = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:xNome", nsNFe))
        
            uf = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:UF", nsNFe))

            valorNFe = checkNone(rootXML.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFe))
            dataImport = date.today()
            dataImport = dataImport.strftime('%d/%m/%Y')

            # DADOS DO ITEM        
            i = 1

            for item in rootXML.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
                #idxItem = item.attrib["nItem"]
                idxItem = i
                cProd = checkNone(item.find(".ns:prod/ns:cProd", nsNFe))
                descricao = checkNone(item.find(".ns:prod/ns:xProd", nsNFe))
                ncm = checkNone(item.find(".ns:prod/ns:NCM", nsNFe))
                cfop = checkNone(item.find(".ns:prod/ns:CFOP", nsNFe))
                vUnitario = checkFloat(item.find(".ns:prod/ns:vUnCom", nsNFe))
                qtde = checkFloat(item.find(".ns:prod/ns:qCom", nsNFe))
                unidade = checkNone(item.find(".ns:prod/ns:uCom", nsNFe))
                vProd = checkFloat(item.find(".ns:prod/ns:vProd", nsNFe))
                vFrete = checkFloat(item.find(".ns:prod/ns:vFrete", nsNFe))
                vSeguro = checkFloat(item.find(".ns:prod/ns:vSeg", nsNFe))
                vDesconto = checkFloat(item.find(".ns:prod/ns:vDesc", nsNFe))
                vOutros = checkFloat(item.find(".ns:prod/ns:vOutro", nsNFe))
                vTotalItem = vProd + vFrete - vDesconto + vOutros
                origem = checkNone(item.find(".ns:imposto/ns:ICMS//ns:orig", nsNFe))

                cICMS = checkNone(item.find(".ns:imposto/ns:ICMS//ns:CSOSN", nsNFe))
                if cICMS == "":
                    cICMS = checkNone(item.find(".ns:imposto/ns:ICMS//ns:CST", nsNFe))

                vBC = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:vBC", nsNFe))
                pICMS = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:pICMS", nsNFe))
                vICMS = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:vICMS", nsNFe))

                pMVAST = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:pMVAST", nsNFe))
                vBCST = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:vBCST", nsNFe))
                pICMSST = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:pICMSST", nsNFe))
                vICMSST = checkFloat(item.find(".ns:imposto/ns:ICMS//ns:vICMSST", nsNFe))

                cIPI = checkNone(item.find(".ns:imposto/ns:IPI//ns:CST", nsNFe))
                vIPI = checkFloat(item.find(".ns:imposto/ns:IPI//ns:vIPI", nsNFe))

                statusNFe = "AUTORIZADA"
                
                item = [numNFe, serie, dataEmissao, chave, tpNF, cnpjEmit, nomeEmit, cnpjDest, cpfDest, nomeDest, uf, valorNFe, 
                        idxItem, cProd, descricao, ncm, cfop, unidade, vUnitario, qtde, vProd, vFrete, vSeguro, vDesconto, vOutros, vTotalItem,
                        origem, cICMS, vBC, pICMS, vICMS, pMVAST, vBCST, pICMSST, vICMSST,
                        cIPI, vIPI, statusNFe, mesAno, dataImport]

                data.append(item)
                i+=1
            
        return data

    def create_df(self, directory):

        i = 0
        listFiles = self.listAllFiles(directory, ".xml")
        df= pd.DataFrame(columns=XML_Cols) 

        print("--- Início processamento ---")
        print("Total de arquivos encontrados a serem processados: {}" .format(len(listFiles)))
    
        for xml in tqdm(listFiles, total=len(listFiles), desc="Processando xmls"):

            #if (i + 100) % 100 == 0:
                #print("Processando lote de {} a {} arquivos ...".format(i + 1, min(i + 100, len(listFiles))))

            for doc in self.readXMLContent(xml):        
                df.loc[len(df)] = doc
        
            i+=1

        print("--- Fim processamento ---")
        return df  


# Classe para leitura do sped ICMS/IPI
class efdReader(docReader):

    efdContent = { }

    def __init__(self) -> None:
        docReader.__init__(self)

        efd_0000 = pd.DataFrame(columns=EFD_Cols["0000"])
        efd_0150 = pd.DataFrame(columns=EFD_Cols["0150"])
        efd_0200 = pd.DataFrame(columns=EFD_Cols["0200"])
        efd_C100 = pd.DataFrame(columns=EFD_Cols["C100"])
        efd_C170 = pd.DataFrame(columns=EFD_Cols["C100"][:8] + ["_DT_INI", "_DT_FIN"] + EFD_Cols["C170"])
        efd_C190 = pd.DataFrame(columns=EFD_Cols["C100"][:8] + ["_DT_INI", "_DT_FIN"] + EFD_Cols["C190"])
        efd_D100 = pd.DataFrame(columns=EFD_Cols["D100"])
        efd_D190 = pd.DataFrame(columns=EFD_Cols["D100"][:11] + ["_DT_INI", "_DT_FIN"] + EFD_Cols["D190"])
        efd_E100 = pd.DataFrame(columns=EFD_Cols["E100"] + EFD_Cols["E110"])
        efd_E111 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_Cols["E111"])
        efd_E116 = pd.DataFrame(columns=EFD_Cols["E100"] + EFD_Cols["E116"])
        efd_E200 = pd.DataFrame(columns=EFD_Cols["E200"] + EFD_Cols["E210"])
        efd_E250 = pd.DataFrame(columns=EFD_Cols["E200"] + EFD_Cols["E250"])
        efd_1900 = pd.DataFrame(columns=EFD_Cols["1900"] + EFD_Cols["1910"] + EFD_Cols["1920"])
        efd_1921 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_Cols["1921"])
        efd_1926 = pd.DataFrame(columns=["_DT_INI", "_DT_FIN"] + EFD_Cols["1926"])

        self.efdContent = { "0000" : efd_0000,
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
       
    def read_all(self, directory):

        i = 1
        listFiles = self.listAllFiles(directory, "txt")
        
        print("--- Início processamento ---")
        print("Total de arquivos encontrados a serem processados: {}" .format(len(listFiles)))
    
        for file in listFiles:

            print(f"{i}: Lendo arquivo: {file} ...")
            self.__read_content(file)        
            i+=1     

        print("--- Fim processamento ---")

        return self.efdContent
            


    def __read_content(self, filename):
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
            
            with open(filename, 'rt', encoding='latin-1') as csvfile:
                leitor_csv = csv.reader(csvfile, delimiter='|')
                total_lines = sum(1 for _ in filename)

                for row in tqdm(leitor_csv, desc="Lendo registros", total=total_lines, unit="linhas"):
                    if row[1] == "0000":
                        self.efdContent["0000"].loc[len(self.efdContent["0000"])] = row[1:-1]
                        
                        # Data da escrituracao
                        dt_inicio = row[4]
                        dt_fim = row[5]

                    elif row[1] == "0150":
                        row = row[1:-1]
                        row.append(dt_inicio)
                        row.append(dt_fim)
                        self.efdContent["0150"].loc[len(self.efdContent["0150"])] = row
                    elif row[1] == "0200":
                        row = row[1:-1]
                        row.append(dt_inicio)
                        row.append(dt_fim)
                        self.efdContent["0200"].loc[len(self.efdContent["0200"])] = row
                    elif row[1] == "C100":
                        row_C100 = row[1:-1]
                        row_C100.append(dt_inicio)
                        row_C100.append(dt_fim)                               
                        self.efdContent["C100"].loc[len(self.efdContent["C100"])] =  row_C100
                    elif row[1] == "C170":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["C170"].loc[len(self.efdContent["C170"])] =  row 
                    elif row[1] == "C190":   
                        head = row_C100[:8] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["C190"].loc[len(self.efdContent["C190"])] =  row 
                    elif row[1] == "D100":
                        row_D100 = row[1:-1]
                        row_D100.append(dt_inicio)
                        row_D100.append(dt_fim)                               
                        self.efdContent["D100"].loc[len(self.efdContent["D100"])] =  row_D100
                    elif row[1] == "D190":
                        head = row_D100[:11] 
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["D190"].loc[len(self.efdContent["D190"])] =  row
                    elif row[1] == "E100":
                        row_E100 = row[1:-1] 
                    elif row[1] == "E110":
                        row = row_E100 + row[1:-1]                          
                        self.efdContent["E100"].loc[len(self.efdContent["E100"])] =  row  
                    elif row[1] == "E111":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["E111"].loc[len(self.efdContent["E111"])] =  row 
                    elif row[1] == "E116":  
                        row = row_E100 + row[1:-1]
                        self.efdContent["E116"].loc[len(self.efdContent["E116"])] =  row      
                    elif row[1] == "E200":
                        row_E200 = row[1:-1] 
                    elif row[1] == "E210":
                        row = row_E200 + row[1:-1]                          
                        self.efdContent["E200"].loc[len(self.efdContent["E200"])] =  row  
                    elif row[1] == "E250":
                        row = row_E200 + row[1:-1] 
                        self.efdContent["E250"].loc[len(self.efdContent["E250"])] =  row 
                    elif row[1] == "1900":
                        row_1900 = row[1:-1] 
                    elif row[1] == "1910":
                        row_1910 = row[1:-1] 
                    elif row[1] == "1920":
                        row = row_1900 + row_1910 + row[1:-1]
                        self.efdContent["1900"].loc[len(self.efdContent["1900"])] =  row 
                    elif row[1] == "1921": 
                        # TODO A DATA DE INICIO PODE SER DIFERENTE NA SUB-APURACAO  
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["1921"].loc[len(self.efdContent["1921"])] =  row 
                    elif row[1] == "1926":   
                        head = []
                        head.append(dt_inicio)
                        head.append(dt_fim) 
                        row = head + row[1:-1]                        
                        self.efdContent["1926"].loc[len(self.efdContent["1926"])] =  row 
                    linha += 1
        except FileNotFoundError as error:
            print(error)
        except Exception as e:
            print(f"Erro ao processar linha {linha}: {e}")
    
    def to_excel(self, filename) -> None:
        try:
            with pd.ExcelWriter(filename) as writer:
                self.efdContent["0000"].to_excel(writer, index=False, sheet_name="0000 - ABERTURA")
                self.efdContent["0150"].to_excel(writer, index=False, sheet_name="0150 - PARTICIPANTES")
                self.efdContent["0200"].to_excel(writer, index=False, sheet_name="0200 - PRODUTOS")
                self.efdContent["C100"].to_excel(writer, index=False, sheet_name="C100 - DOC")
                self.efdContent["C170"].to_excel(writer, index=False, sheet_name="C170 - ITENS")
                self.efdContent["C190"].to_excel(writer, index=False, sheet_name="C190 - TOTALIZADORES")
                self.efdContent["D100"].to_excel(writer, index=False, sheet_name="D100 - TRANSPORTE")
                self.efdContent["D190"].to_excel(writer, index=False, sheet_name="D190 - TRANSP. TOTAL")
                self.efdContent["E100"].to_excel(writer, index=False, sheet_name="E100 - APURACAO ICMS")
                self.efdContent["E111"].to_excel(writer, index=False, sheet_name="E111 - AJUSTES ICMS")
                self.efdContent["E116"].to_excel(writer, index=False, sheet_name="E116 - OBRIG ICMS")
                self.efdContent["E200"].to_excel(writer, index=False, sheet_name="E200 - APURACAO ICMS-ST")
                self.efdContent["E250"].to_excel(writer, index=False, sheet_name="E250 - OBRIG ICMS-ST") 
                self.efdContent["1900"].to_excel(writer, index=False, sheet_name="1900 - SUB-APURACAO ICMS")  
                self.efdContent["1921"].to_excel(writer, index=False, sheet_name="1921 - AJUSTES SUB-AP") 
                self.efdContent["1926"].to_excel(writer, index=False, sheet_name="1926 - OBRIG SUB-APURACAO")
        except Exception as e:
            print(f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {e}")
            
def export_efd(input_dir, output_dir):
    
    try:
        efd_reader = efdReader()
        efd_reader.read_all(input_dir)
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(output_dir, f"efd_export_{dt}.xlsx")
        print(f"Exportando dados para o arquivo excel:{filename}")
        efd_reader.to_excel(filename) 
        print("Concluído!")

    except FileNotFoundError:
        print(f"Arquivo '{input_dir}' não encontrado.")
    except Exception as e:
        print(f"Erro não esperado: {e}")


def export_nfe(input_dir, output_dir):
    
    try:
        xml_reader = XMLReader()

        df_new = xml_reader.create_df(input_dir)
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(output_dir, f"nfe_export_{dt}.xlsx")
        print(f"Exportando dados para o arquivo excel:{filename}")
        if df_new.size > 0:
            df_new.to_excel(filename, index=False)
        print("Concluído!")

    except FileNotFoundError:
        print(f"Arquivo '{input_dir}' não encontrado.")

    except Exception as e:
        print(f"Erro não esperado: {e}")


def remove_signature(input_dir, output_dir):    

    # Lista todos os arquivos TXT na pasta
    arquivos_txt = [arquivo for arquivo in os.listdir(input_dir) if arquivo.lower().endswith(".txt")]

    # Processa cada arquivo
    for arquivo in arquivos_txt:
        caminho_arquivo = os.path.join(input_dir, arquivo)
        with open(caminho_arquivo, "r", encoding='latin-1') as arquivo_original:
            linhas = arquivo_original.readlines()

        i = 0
        for linha in linhas:
            if linha.startswith("|9999|"):
                break
            else:   
                i+=1
        
        # Remove a assinatura digital apos registro 9999
        linhas = linhas[:i]

        # Salva o conteúdo modificado em um novo arquivo
        novo_caminho_arquivo = os.path.join(output_dir, f"sem_assinatura_{arquivo}")
        with open(novo_caminho_arquivo, "w", encoding="latin-1") as novo_arquivo:
            novo_arquivo.writelines(linhas)

        print(f"Arquivo {arquivo} processado. Assinatura digital removida e salva em {novo_caminho_arquivo}")

    print("Processo concluído.")



