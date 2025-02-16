import streamlit as st
import pandas as pd
from spedlib import EFDReader, EFD_LAYOUT
from io import BytesIO
import os

# Função para exportar DataFrame para Excel
def export_to_excel(dataframes, selected_records):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for record in selected_records:
            if record in dataframes:
                sheet_name = EFD_LAYOUT[record][1]
                dataframes[record].to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output

# Título do aplicativo
st.title("Exportador de Registros SPED para Excel")

# Upload do arquivo SPED
uploaded_file = st.file_uploader("Carregar arquivo SPED (.txt)", type="txt")

if uploaded_file:
    # Instância do leitor de SPED
    reader = EFDReader(encoding="latin-1")

    # Lê o conteúdo do arquivo
    try:
        # Salva o arquivo carregado temporariamente
        temp_file_path = os.path.join(os.getcwd(), "uploaded_file.txt")
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Processa o arquivo
        reader.read_from_path(os.getcwd())

        # Lista de registros disponíveis
        available_records = list(reader.data.keys())

        # Seletor de registros
        selected_records = st.multiselect(
            "Selecione os registros que deseja exportar:",
            options=available_records,
            default=available_records
        )

        # Botão para exportar
        if st.button("Exportar para Excel"):
            excel_data = export_to_excel(reader.data, selected_records)
            st.download_button(
                label="Baixar Excel",
                data=excel_data,
                file_name="registros_selecionados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

    finally:
        # Remove o arquivo temporário após o processamento
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
