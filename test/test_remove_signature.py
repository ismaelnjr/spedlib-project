import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib import remove_signature, list_all_files

class NFeExportTest(unittest.TestCase):

    def test_remove_signature(self):
        
        input_dir = f"{path}\\test_data\\input\\sped"
        output_dir = f"{path}\\test_data\\output"
        
        files = list_all_files(input_dir, ".txt")
        for file in files:
            output_file = os.path.join(output_dir, "sem_assinatura_" + os.path.basename(file))
            remove_signature(file, output_file)
        
        self.assertTrue(os.path.exists(output_file))        
           
if __name__ == '__main__':
    unittest.main()