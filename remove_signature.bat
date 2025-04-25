@echo off
REM === Validação dos argumentos ===
IF "%~1"=="" (
    echo [ERRO] Informe o diretorio de origem
    echo Uso: remove_signarture.bat INPUT_DIR
    exit /b 1
)

SET "INPUT_DIR=%~1"

echo Executando: python remove_signature.py %INPUT_DIR% 
python remove_signature.py "%INPUT_DIR%"