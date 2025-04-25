import os
import argparse
from datetime import datetime

from spedlib.utils import remove_efd_signature, list_all_files

def main(input_dir, output_dir):
    
    files = list_all_files(input_dir, ".txt")
    for file in files:
        output_file = os.path.join(output_dir, "sem_assinatura_" + os.path.basename(file))
        remove_efd_signature(file, output_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Exporta dados da NFe para uma planilha Excel')
    parser.add_argument(
        'input_dir', 
        metavar='INPUT_DIR', 
        type=str,
        help='Caminho da pasta com os arquivos XML da NFe'
    )
    parser.add_argument(
        'output_dir', 
        metavar='OUTPUT_DIR', 
        type=str,
        nargs='?',  # <- torna o argumento posicional opcional
        default='.\\sem_assinatura',
        help='(Opcional) Caminho da pasta destino com os arquivos XML da NFe (padrão: .\\sem_assinatura)'
    )
    args = parser.parse_args()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)    
    
    if not os.path.exists(args.input_dir):
        print(f"[ERRO] Pasta {args.input_dir} nao encontrada.")
    else:
        main(args.input_dir, args.output_dir)

