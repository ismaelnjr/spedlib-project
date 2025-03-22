import unittest
import os
import sys
from datetime import datetime

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib.efd_export import EFDExport
from spedlib.efd_reader import EFDReader

class NFeExportTest(unittest.TestCase):

    def test_export_efd(self):
        
        efd_reader = EFDReader(encoding="latin-1")
        input_dir = f"{path}\\test_data\\input\\sped"
                
        output_dir = f"{path}\\test_data\\output"
        efd_reader.read_from_path(input_dir)        
        
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(output_dir, f"efd_export_{dt}.xlsx")
        
        export_efd = EFDExport(efd_reader)
        export_efd.to_excel(filename)
        
        self.assertTrue(os.path.exists(filename))
           
if __name__ == '__main__':
    unittest.main()