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



