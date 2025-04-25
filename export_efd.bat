@echo off
REM === Validação dos argumentos ===
IF "%~1"=="" (
    echo [ERRO] Informe o diretorio de origem
    echo Uso: export_efd.bat INPUT_DIR
    exit /b 1
)

SET "INPUT_DIR=%~1"

echo Executando: python export_efd.py %INPUT_DIR% 
python export_efd.py "%INPUT_DIR%"