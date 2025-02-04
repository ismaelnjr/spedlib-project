import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib import export_efd

class NFeExportTest(unittest.TestCase):

    def test_export_efd(self):
        
        input_dir = f"{path}\\test_data\\input\\higietop"
        output_dir = f"{path}\\test_data\\output"
        export_efd(input_dir, output_dir)
           
if __name__ == '__main__':
    unittest.main()