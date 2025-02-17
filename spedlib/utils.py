import os


# Funções genéricas para tratamento de dados
def check_none(var):
    if var == None:
        return ""
    else:
        try:
            return var.text.replace('.',',')
        except:
            return var.text

def check_int(var):
    if var == None:
        return 0
    else:
        try:
            return int(var.text)
        except:
            return 0

def check_float(var):
    if var == None:
        return 0.0
    else:
        try:
            return float(var.text)
        except:
            return 0.0

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

        files = []

        for f in os.listdir(current_dir):
            if f.lower().endswith(file_ext):
                files.append(os.path.join(current_dir, f))
        
        return files
        

def remove_signature(input_file, output_file, encoding='latin-1'):    

    with open(input_file, "r", encoding=encoding) as arquivo_original:
        linhas = arquivo_original.readlines()

    i = 0
    for linha in linhas:
        if linha.startswith("|9999|"):
            break
        else:   
            i+=1
        
    # Remove a assinatura digital apos registro 9999
    linhas = linhas[:i]
    with open(output_file, "w", encoding="latin-1") as novo_arquivo:
        novo_arquivo.writelines(linhas)
        print(f"Assinatura digital removida e salva em {output_file}")

  





