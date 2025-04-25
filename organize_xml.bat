@echo off
REM === Validação dos argumentos ===
IF "%~1"=="" (
    echo [ERRO] Informe o diretorio de origem
    echo Uso: organize_xml.bat INPUT_DIR
    exit /b 1
)

SET "INPUT_DIR=%~1"

echo Executando: python organize_xml.py %INPUT_DIR% 
python organize_xml.py "%INPUT_DIR%"