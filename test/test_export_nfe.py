import unittest
import os
import sys
from datetime import datetime

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib import NFEReader, NFeExport

class NFeExportTest(unittest.TestCase):

    def test_export_nfe(self):
        
        nfe_reader = NFEReader()
        input_dir = f"{path}\\test_data\\input\\nfe"
        output_dir = f"{path}\\test_data\\output"
        nfe_reader.read_from_path(input_dir)
        
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(output_dir, f"nfe_export_{dt}.xlsx")
        
        export_nfe = NFeExport(nfe_reader)
        export_nfe.to_excel(filename)     
    
        self.assertTrue(os.path.exists(filename))
          
if __name__ == '__main__':
    unittest.main()