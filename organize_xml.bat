@echo off
REM === Validação dos argumentos ===
IF "%~1"=="" (
    echo [ERRO] Informe o diretorio de origem
    echo Uso: organize_xml.bat INPUT_DIR OUTPUT_DIR
    exit /b 1
)
IF "%~2"=="" (
    echo [ERRO] Informe o diretorio de destino
    echo Uso: organize_xml.bat INPUT_DIR OUTPUT_DIR
    exit /b 1
)

SET "INPUT_DIR=%~1"
SET "OUTPUT_DIR=%~2"

echo Executando: python organize_xml.py %INPUT_DIR% 
python organize_xml.py "%INPUT_DIR%" "%OUTPUT_DIR%"