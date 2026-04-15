import streamlit as st
import pandas as pd
from spedlib.efd_reader import EFDReader, EFD_LAYOUT
from spedlib.utils import remove_efd_signature
from io import BytesIO
import os
from datetime import datetime
import tempfile
import hashlib
import time


def get_exportable_records(dataframes, selected_records, skip_empty=True):
    exportable_records = []
    for record in selected_records:
        if record not in dataframes:
            continue

        df = dataframes[record]
        if skip_empty and df.empty:
            continue

        exportable_records.append(record)

    return exportable_records


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
    records_to_export = get_exportable_records(dataframes, selected_records, skip_empty=True)
    if not records_to_export:
        raise ValueError("Nenhum registro com dados para exportar.")

    started_at = time.perf_counter()
    output = BytesIO()
    sheets_written = 0
    total_rows = 0
    with pd.ExcelWriter(
        output,
        engine="xlsxwriter",
        engine_kwargs={"options": {"strings_to_urls": False}},
    ) as writer:
        for record in records_to_export:
            sheet_name = EFD_LAYOUT[record][1]
            df = dataframes[record]
            total_rows += len(df)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            sheets_written += 1

    output.seek(0)
    elapsed_seconds = time.perf_counter() - started_at
    return output, {
        "sheets_written": sheets_written,
        "rows_written": total_rows,
        "elapsed_seconds": elapsed_seconds,
    }

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
            ui_state = {"last_ui_update": 0.0, "last_shown_percent": -1}

            def on_progress(processed_lines, total_lines, percent, elapsed_seconds, eta_seconds):
                now = time.monotonic()
                progress_value = min(max(int(percent), 0), 100) if percent is not None else 0
                should_update = (
                    progress_value >= ui_state["last_shown_percent"] + 1
                    or (now - ui_state["last_ui_update"]) >= 1.0
                    or progress_value == 100
                )
                if not should_update:
                    return

                ui_state["last_ui_update"] = now
                ui_state["last_shown_percent"] = progress_value
                progress_bar.progress(progress_value)

                if total_lines:
                    processed_text = f"Processado {processed_lines}/{total_lines} linhas"
                else:
                    processed_text = f"Processado {processed_lines} linhas"

                status_text.info(
                    f"{processed_text} ({percent:.2f}%) - "
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
        non_empty_records = get_exportable_records(data, available_records, skip_empty=True)

        # Seletor de registros
        selected_records = st.multiselect(
            "Selecione os registros que deseja exportar:",
            options=available_records,
            default=non_empty_records,
        )
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        # Botão para exportar
        if st.button("Exportar para Excel"):
            export_status = st.empty()
            export_status.info("Gerando arquivo Excel, aguarde...")
            records_to_export = get_exportable_records(data, selected_records, skip_empty=True)
            if not records_to_export:
                export_status.warning("Nenhum registro com dados foi selecionado para exportação.")
            else:
                excel_data, export_metrics = export_to_excel(data, records_to_export)
                export_status.success("Arquivo Excel gerado com sucesso.")
                st.caption(
                    "Exportacao concluida em "
                    f"{format_duration(export_metrics['elapsed_seconds'])} - "
                    f"{export_metrics['sheets_written']} abas e "
                    f"{export_metrics['rows_written']} linhas."
                )
                st.download_button(
                    label="Baixar Excel",
                    data=excel_data,
                    file_name=f"efd_export_{dt}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
