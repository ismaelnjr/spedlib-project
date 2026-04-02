import streamlit as st
import pandas as pd
from spedlib.efd_reader import EFDReader, EFD_LAYOUT
from spedlib.utils import remove_efd_signature
from io import BytesIO
import os
from datetime import datetime
import tempfile
import hashlib

def create_temp_file(content, filename, session_id):
    suffix = f"_{session_id}_{os.path.basename(filename)}.efd_data"
    fd, temp_file = tempfile.mkstemp(suffix=suffix)
    os.close(fd)

    # Salva o arquivo carregado temporariamente
    with open(temp_file, "wb") as f:
        f.write(content)

    # Remove a assinatura digital
    remove_efd_signature(temp_file, temp_file)

    return temp_file

def read_data(file_content, filename, file_hash, _progress_callback=None):
    del file_hash  # usado apenas como chave de cache
    session_id = st.session_state.setdefault("session_id", hashlib.sha256(os.urandom(16)).hexdigest()[:10])
    temp_file = create_temp_file(file_content, filename, session_id)
    try:
        reader = EFDReader(encoding="latin-1")
        reader.read_file(temp_file, progress_callback=_progress_callback)
        return reader.data
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def format_duration(seconds: float) -> str:
    total_seconds = max(int(seconds), 0)
    minutes, secs = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

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
st.title("Exportador de Registros SPED ICMS/IPI para Excel")

# Upload do arquivo SPED
uploaded_file = st.file_uploader("Carregar arquivo SPED (.txt)", type="txt")

if uploaded_file:
    try:
        file_content = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_content).hexdigest()
        parsed_data = st.session_state.get("parsed_data")

        # Processa novamente apenas quando o arquivo muda.
        if st.session_state.get("last_uploaded_hash") != file_hash or parsed_data is None:
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.info("Iniciando leitura do arquivo...")

            def on_progress(processed_lines, total_lines, percent, elapsed_seconds, eta_seconds):
                progress_value = min(max(int(percent), 0), 100)
                progress_bar.progress(progress_value)
                status_text.info(
                    f"Processado {processed_lines}/{total_lines} linhas ({percent:.2f}%) - "
                    f"ETA: {format_duration(eta_seconds)} - "
                    f"Tempo decorrido: {format_duration(elapsed_seconds)}"
                )

            parsed_data = read_data(
                file_content=file_content,
                filename=uploaded_file.name,
                file_hash=file_hash,
                _progress_callback=on_progress,
            )
            st.session_state["parsed_data"] = parsed_data
            st.session_state["last_uploaded_hash"] = file_hash
            progress_bar.progress(100)
            status_text.success("Leitura concluida com sucesso.")

        data = parsed_data
        
        # Lista de registros disponíveis
        available_records = list(data.keys())

        # Seletor de registros
        selected_records = st.multiselect(
            "Selecione os registros que deseja exportar:",
            options=available_records,
            default=available_records
        )
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        # Botão para exportar
        if st.button("Exportar para Excel"):
            export_status = st.empty()
            export_status.info("Gerando arquivo Excel, aguarde...")
            excel_data = export_to_excel(data, selected_records)
            export_status.success("Arquivo Excel gerado com sucesso.")
            st.download_button(
                label="Baixar Excel",
                data=excel_data,
                file_name=f"efd_export_{dt}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
