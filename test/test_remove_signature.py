import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib import remove_signature

class NFeExportTest(unittest.TestCase):

    def test_remove_signature(self):
        
        input_dir = f"{path}\\test_data\\input\\sped"
        output_dir = f"{path}\\test_data\\output"
        remove_signature(input_dir, output_dir)
           
if __name__ == '__main__':
    unittest.main()