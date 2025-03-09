import os
import zipfile
import random
import string
import shutil
 
from pathlib import Path
import xml.etree.ElementTree as ET

default_folders_map = {'nfe': 'nfe', 'canc': 'canc', 'cce': 'cce', 'inut': 'inut'}

def format_cnpj(cnpj):
    if cnpj == "":
        return ""
    try:
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
        return cnpj
    except:
        return ""
        
def format_cpf(cpf):
    if cpf == "":
        return ""
    try:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    except:
        return ""

def list_all_files(current_dir, file_ext):
    """List all files in a directory with a specific extension."""
    files = []
    for f in os.listdir(current_dir):
        if f.lower().endswith(file_ext):
            files.append(os.path.join(current_dir, f))        
    return files        

def remove_efd_signature(input_efd_file, output_efd_file, encoding='latin-1'):    
    """Remove a assinatura digital de um arquivo EFD"""
    with open(input_efd_file, "r", encoding=encoding) as arquivo_original:
        linhas = arquivo_original.readlines()
    i = 0
    for linha in linhas:
        if linha.startswith("|9999|"):
            break
        else:   
            i+=1
        
    # Remove a assinatura digital apos registro 9999
    linhas = linhas[:i]
    with open(output_efd_file, "w", encoding="latin-1") as novo_arquivo:
        novo_arquivo.writelines(linhas)
        print(f"Assinatura digital removida e salva em {output_efd_file}")
 
 
def organize_xmls(source_dir_fd: str, dest_dir_fd: str, folders_map=default_folders_map):
    """organiza os arquivos xml contidos em uma pasta e os move para subpastas de 
    um diretório fornecido pelo usuário """ 
    
    def _create_folders(path: str, dest_fds_map: dict):
        """Cria as pastas necessárias para armazenar os arquivos XML."""    
        if not os.path.exists(path):
            os.makedirs(path)

        for key in dest_fds_map:
            if not os.path.exists(f"{path}\\{dest_fds_map[key]}"):
                os.makedirs(f"{path}\\{dest_fds_map[key]}")

    _create_folders(dest_dir_fd, folders_map)
    for root, dirs, files in os.walk(source_dir_fd):
        for file in files:
            file_path = Path(root) / file
            if file.endswith('.zip'):
                temp_folder = Path.cwd() / ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
                extract_xmls(file_path, temp_folder)
                organize_xmls(source_dir_fd=temp_folder, dest_dir_fd=dest_dir_fd, folders_map=folders_map)
                shutil.rmtree(temp_folder)
            elif file.endswith('.xml'):
                try:
                    xml_type = get_xml_type(file_path)
                    if xml_type == 'undefined':
                        print(f"Arquivo {file} não é um arquivo xml conhecido")
                    else:
                        file_path.rename(Path(dest_dir_fd) / folders_map[xml_type] / file)
                except Exception as e:
                    print(f"Erro ao processar {file}: {e}")                        

def find_all_xmls(from_path, xml_types: list = ['nfe', 'canc', 'cce', 'inut']):
    """Finds and returns a list of NFE XML files from a specified directory.

    This static method traverses the directory tree starting from `from_path`, 
    searching for files with an '.xml' extension. It identifies files of types 
    'nfe', 'canc', 'cce', and 'inut', collecting their paths in a list which 
    is returned at the end.

    Args:
        from_path (str): The root directory path to start the search from.
        xml_types (list, optional): A list of XML types to filter the results. 
            Defaults to ['nfe', 'canc', 'cce', 'inut'].

    Returns:
        list: A list of paths to the NFE XML files found in the directory.
    """

    nfe_list = []
    for file_path in Path(from_path).rglob('*.xml'):
        xml_type = get_xml_type(file_path)
        if xml_type in xml_types:
            nfe_list.append(file_path) 
    return nfe_list


def extract_xmls(zipFile: str, dest_dir_fd: str):
    """extrai os arquivos xml de um arquivo zip para um diretório fornecido pelo usuário"""    
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        zip_ref.extractall(dest_dir_fd)
        
def get_xml_type(xml_file):
    """determina o tipo de um arquivo xml"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    if root.tag == '{http://www.portalfiscal.inf.br/nfe}nfeProc':
        return 'nfe'
    elif root.tag == '{http://www.portalfiscal.inf.br/nfe}procEventoNFe':
        tipo_evento = root.find('.//nfe:tpEvento', ns).text
        return {'110111': 'canc', '110110': 'cce'}.get(tipo_evento, 'undefined')
    elif root.tag == '{http://www.portalfiscal.inf.br/nfe}retInutNFe':
        return 'inut'
    return 'undefined'  





