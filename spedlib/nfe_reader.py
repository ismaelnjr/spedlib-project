from tqdm import tqdm
from datetime import date
from .utils import check_float, check_none, format_cnpj, format_cpf, list_all_files
import xml.etree.ElementTree as et
import pandas as pd


# Dicionário com colunas de uma NFe
NFE_LAYOUT = [ "NUM_NFE",
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
                "NITEM",
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

     
# Classe para leitura de NFe (modelo 55)
class NFEReader():

    _data= pd.DataFrame(columns=NFE_LAYOUT) 

    def __init__(self) -> None:
        pd.options.display.float_format = "{:,.2f}".format

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    def _read_nfe_content(self, xml):
        
        data = []
        rootXML = et.parse(xml).getroot()
        
        if "nfeProc" in rootXML.tag:
                 
            nsNFe = {"ns": "http://www.portalfiscal.inf.br/nfe"}

            # DADOS DA NFE        
            numNFe = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF" , nsNFe))
            serie = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFe))
            dataEmissao = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe))
            dataEmissao = F"{dataEmissao[8:10]}/{dataEmissao[5:7]}/{dataEmissao[:4]}"
            if check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:ide/ns:tpNF", nsNFe)) == 0:
                tpNF = "ENTRADA"
            else:
                tpNF = "SAIDA"
            
            mesAno = F"{dataEmissao[-4:]}_{dataEmissao[3:5]}"
            
            chave = check_none(rootXML.find("./ns:protNFe/ns:infProt/ns:chNFe", nsNFe))
            cnpjEmit = format_cnpj (check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ", nsNFe)))
            nomeEmit = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:emit/ns:xNome", nsNFe))
            
            cnpjDest = format_cnpj(check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ", nsNFe)))
            cpfDest = format_cpf (check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:CPF", nsNFe)))
            nomeDest = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:xNome", nsNFe))
        
            uf = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:UF", nsNFe))

            valorNFe = check_none(rootXML.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFe))
            dataImport = date.today()
            dataImport = dataImport.strftime('%d/%m/%Y')

            # DADOS DO ITEM        
            i = 1

            for item in rootXML.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
                #idxItem = item.attrib["nItem"]
                idxItem = i
                cProd = check_none(item.find(".ns:prod/ns:cProd", nsNFe))
                descricao = check_none(item.find(".ns:prod/ns:xProd", nsNFe))
                ncm = check_none(item.find(".ns:prod/ns:NCM", nsNFe))
                cfop = check_none(item.find(".ns:prod/ns:CFOP", nsNFe))
                vUnitario = check_float(item.find(".ns:prod/ns:vUnCom", nsNFe))
                qtde = check_float(item.find(".ns:prod/ns:qCom", nsNFe))
                unidade = check_none(item.find(".ns:prod/ns:uCom", nsNFe))
                vProd = check_float(item.find(".ns:prod/ns:vProd", nsNFe))
                vFrete = check_float(item.find(".ns:prod/ns:vFrete", nsNFe))
                vSeguro = check_float(item.find(".ns:prod/ns:vSeg", nsNFe))
                vDesconto = check_float(item.find(".ns:prod/ns:vDesc", nsNFe))
                vOutros = check_float(item.find(".ns:prod/ns:vOutro", nsNFe))
                vTotalItem = vProd + vFrete - vDesconto + vOutros
                origem = check_none(item.find(".ns:imposto/ns:ICMS//ns:orig", nsNFe))

                cICMS = check_none(item.find(".ns:imposto/ns:ICMS//ns:CSOSN", nsNFe))
                if cICMS == "":
                    cICMS = check_none(item.find(".ns:imposto/ns:ICMS//ns:CST", nsNFe))

                vBC = check_float(item.find(".ns:imposto/ns:ICMS//ns:vBC", nsNFe))
                pICMS = check_float(item.find(".ns:imposto/ns:ICMS//ns:pICMS", nsNFe))
                vICMS = check_float(item.find(".ns:imposto/ns:ICMS//ns:vICMS", nsNFe))

                pMVAST = check_float(item.find(".ns:imposto/ns:ICMS//ns:pMVAST", nsNFe))
                vBCST = check_float(item.find(".ns:imposto/ns:ICMS//ns:vBCST", nsNFe))
                pICMSST = check_float(item.find(".ns:imposto/ns:ICMS//ns:pICMSST", nsNFe))
                vICMSST = check_float(item.find(".ns:imposto/ns:ICMS//ns:vICMSST", nsNFe))

                cIPI = check_none(item.find(".ns:imposto/ns:IPI//ns:CST", nsNFe))
                vIPI = check_float(item.find(".ns:imposto/ns:IPI//ns:vIPI", nsNFe))

                statusNFe = "AUTORIZADA"
                
                item = [numNFe, serie, dataEmissao, chave, tpNF, cnpjEmit, nomeEmit, cnpjDest, cpfDest, nomeDest, uf, valorNFe, 
                        idxItem, cProd, descricao, ncm, cfop, unidade, vUnitario, qtde, vProd, vFrete, vSeguro, vDesconto, vOutros, vTotalItem,
                        origem, cICMS, vBC, pICMS, vICMS, pMVAST, vBCST, pICMSST, vICMSST,
                        cIPI, vIPI, statusNFe, mesAno, dataImport]

                data.append(item)
                i+=1
            
        return data

    def read_from_path(self, path, file_ext = ".xml"):
        xml_files = list_all_files(path, file_ext)
        return self.read_files(xml_files)
        
    def read_files(self, xml_files: list[str]) :

        print("--- Início processamento ---")
        print("Total de arquivos encontrados a serem processados: {}" .format(len(xml_files)))
    
        for xml in tqdm(xml_files, total=len(xml_files), desc="Processando xmls"):

            for doc in self._read_nfe_content(xml):        
                self._data.loc[len(self._data)] = doc        

        print("--- Fim processamento ---")

    
