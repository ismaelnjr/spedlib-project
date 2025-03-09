import unittest
import os
import sys
from datetime import datetime

# Necessário para que o arquivo de testes encontre
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path.insert(0, os.path.dirname(path))
sys.path.insert(0, path)

from spedlib.utils import extract_xmls, organize_xmls

class NFeUtilsTest(unittest.TestCase):
    
    def test_organize_nfe(self):
        
        input_dir = f"{path}\\test_data\\input\\zips"
        output_dir = f"{path}\\test_data\\output\\graef"
                
        organize_xmls( source_dir_fd=input_dir, dest_dir_fd=output_dir) 
        self.assertTrue(os.path.exists(f"{output_dir}\\nfe\\nfe1.xml"))
          
if __name__ == '__main__':
    unittest.main()