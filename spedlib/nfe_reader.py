import json
import xml.etree.ElementTree as ET
import os
import pandas as pd

from datetime import date
from tqdm import tqdm
from .utils import format_cnpj, format_cpf, list_all_files

path = os.path.dirname(os.path.abspath(__file__))

# Carregar layout da NFe
def load_nfe_layout(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

NFE_LAYOUT_CONFIG = load_nfe_layout(f'{path}\\cfg\\nfe_layout.json')

def get_columns_by_group(group: list):
    return [(col, config) for col, config in NFE_LAYOUT_CONFIG["columns"].items() if config["group"] in group]

# Funções auxiliares
def parse_element(element, value_type, default_value=None):
    if element is None:
        if default_value is not None:
            return default_value
        return "" if value_type == "string" else 0
    try:
        if value_type == "int":
            return int(element.text)
        elif value_type == "float":
            return float(element.text)
        elif value_type == "string":
            return element.text
    except:
        if default_value is not None:
            return default_value
        return "" if value_type == "string" else 0

def date_parser(value):
    if value:
        return f"{value[8:10]}/{value[5:7]}/{value[:4]}"
    return ""

def calculate_total_item(vProd, vFrete, vSeguro, vDesc, vOutros):
    return vProd + vFrete + vSeguro - vDesc + vOutros

def calculate_mes_ano(date_str):
    return f"{date_str[-4:]}_{date_str[3:5]}"

FUNCTIONS = {
    "calculate_total_item": calculate_total_item,
    "calculate_mes_ano": calculate_mes_ano,
    "now": lambda: date.today().strftime('%d/%m/%Y')
}

PARSERS = {
    "date_parser": date_parser,
    "cnpj_parser": format_cnpj,
    "cpf_parser": format_cpf
}

def find_element_with_multiple_paths(item, config, nsNFe):
    if config.get("path"):
        element = item.find(config["path"], nsNFe)
        if element is not None:
            return element
    if config.get("paths"):
        for path_option in config["paths"]:
            element = item.find(path_option, nsNFe)
            if element is not None:
                return element
    return None

class NFEReader:

    def __init__(self):
        pd.options.display.float_format = "{:,.2f}".format
        self._data = None

    @property
    def data(self):
        return self._data

    def read_nfe(self, filename):
        rootXML = ET.parse(filename).getroot()
        nsNFe = {"ns": NFE_LAYOUT_CONFIG["ns"]}

        data = []
        if "nfeProc" in rootXML.tag:
            nfe_data = {}
            for col, config in get_columns_by_group(["cabecalho"]):
                if config.get("atrib"):
                    value = rootXML.attrib.get(config["atrib"])
                    nfe_data[col] = value
                elif config.get("path") or config.get("paths"):
                    element = find_element_with_multiple_paths(rootXML, config, nsNFe)
                    default_value = config.get("default")
                    value = parse_element(element, config["type"], default_value)
                    nfe_data[col] = value
                elif config.get("function"):
                    args = [nfe_data.get(arg, 0) for arg in config.get("args", [])]
                    nfe_data[col] = FUNCTIONS[config["function"]](*args)

                if config.get("parser"):
                    nfe_data[col] = PARSERS[config["parser"]](nfe_data[col])

            for idx, item in enumerate(rootXML.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe)):
                item_data = nfe_data.copy()

                for col, config in get_columns_by_group(["item", "imposto", "finalizador"]):
                    if config.get("atrib"):
                        value = item.attrib.get(config["atrib"])
                        item_data[col] = value
                    elif config.get("path") or config.get("paths"):
                        element = find_element_with_multiple_paths(item, config, nsNFe)
                        default_value = config.get("default")
                        value = parse_element(element, config["type"], default_value)
                        item_data[col] = value
                    elif config.get("function"):
                        args = [item_data.get(arg, 0) for arg in config.get("args", [])]
                        item_data[col] = FUNCTIONS[config["function"]](*args)

                    if config.get("parser"):
                        item_data[col] = PARSERS[config["parser"]](item_data[col])

                data.append(item_data)
        return data

    def read_all(self, files, verbose=True):
        print("--- Início processamento ---")
        print(f"Total de arquivos encontrados a serem processados: {len(files)}")

        data = []
        for xml in tqdm(files, total=len(files), desc="Processando xmls", disable=not verbose):
            for doc in self.read_nfe(xml):
                data.append(doc)

        print("--- Fim processamento ---")
        return data

    def read_from_path(self, path, file_ext=".xml"):
        xml_files = list_all_files(path, file_ext)
        self._data = pd.DataFrame(self.read_all(xml_files), columns=NFE_LAYOUT_CONFIG["columns"])
        return self.data
