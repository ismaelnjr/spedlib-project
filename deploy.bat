@echo off
REM Deploy modulo python

REM 1. Limpar builds anteriores
echo Limpando builds anteriores...
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q *.egg-info

REM 2. Gerar novo pacote
echo Gerando pacote...
python setup.py sdist bdist_wheel 

REM 3. Fazer upload para o PyPI
echo Fazendo upload para o PyPI...
pause
twine upload dist/*

REM 4. Finalizando
echo Deploy concluido!
pause 