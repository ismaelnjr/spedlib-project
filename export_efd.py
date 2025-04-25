import os
import argparse
from datetime import datetime

from spedlib.efd_reader import EFDReader
from spedlib.efd_export import EFDExport

def export_nfe(input_dir, output_dir):
    
    efd_reader = EFDReader(encoding="latin-1")
    efd_reader.read_from_path(input_dir)        
    
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(output_dir, f"efd_export_{dt}.xlsx")
    
    export_efd = EFDExport(efd_reader)
    export_efd.to_excel(filename)   

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
        export_nfe(args.input_dir, args.output_dir)

