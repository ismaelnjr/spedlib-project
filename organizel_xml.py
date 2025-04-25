import os
import argparse

from spedlib.utils import organize_xmls

def main(input_dir, output_dir):
    
    organize_xmls( source_dir_fd=input_dir, dest_dir_fd=output_dir, copy_files=True) 

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
        default='.\\output',
        help='Caminho da pasta destino com os arquivos XML da NFe'
    )
    args = parser.parse_args()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)    

    if not os.path.exists(args.input_dir):
        print(f"[ERRO] Pasta {args.input_dir} nao encontrada.")
    else:
        main(args.input_dir, args.output_dir)

