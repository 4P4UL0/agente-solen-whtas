# streamlit_app/memoria_manager.py

import os
import sys
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import logging

# 👉 Corrige o sys.path para encontrar vectorstore_manager.py que está na raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora o import funciona normalmente
import vectorstore_manager as vt

# Configurações
VECTORSTORE_DIR = "vectorstore"
DOCUMENTOS_DIR = "streamlit_app/documentos"
PROCESSED_FILES_PATH = "streamlit_app/processed_files.txt"

# Configuração de logging
logging.basicConfig(
    filename='streamlit_app/memoria_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cria os diretórios necessários
os.makedirs(DOCUMENTOS_DIR, exist_ok=True)
os.makedirs(VECTORSTORE_DIR, exist_ok=True)
os.makedirs("streamlit_app/logs", exist_ok=True)

def login():
    """Função de login com verificação de senha."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='color: #1f2937; text-align: center;'>Bem-vindo</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6b7280; text-align: center;'>Faça login para atualizar os dados</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            senha = st.text_input("🔒 Senha", type="password", key='login_pass')
            submit_button = st.form_submit_button("Entrar")
            if submit_button:
                if senha == "boom@2025":
                    st.session_state.logged_in = True
                    st.success("✅ Acesso autorizado!")
                    st.rerun()
                else:
                    st.error("🚫 Credenciais inválidas.")
        st.caption("Problemas para acessar? Contate o suporte")

def processar_pdf(file_path):
    """Extrai texto do PDF e divide em chunks."""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            if not text.strip():
                logging.warning(f"Nenhum texto em {os.path.basename(file_path)}")
                return None
            metadata = {"fonte": os.path.basename(file_path)}
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            return text_splitter.create_documents([text], [metadata])
    except Exception as e:
        logging.error(f"Erro no arquivo {file_path}: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Gerenciador de Memória - Solem",
        page_icon="🛠️",
        layout="wide"
    )
    st.title("🛠️ Gerenciador de Memória Solem")
    
    # Status da memória
    st.header("📊 Status")
    if vt.verificar_arquivos_memoria():
        st.success("✅ Memória válida")
        try:
            with open(PROCESSED_FILES_PATH, 'r') as f:
                arquivos = f.readlines()
            st.write(f"Documentos processados: {len(arquivos)}")
        except Exception:
            st.write("Nenhum documento processado.")
    else:
        st.error("❌ Memória incompleta")
    
    # Seção para reparo (função unificada)
    st.header("🔧 Reparar Memória")
    if st.button("🛠️ Reparar .pkl"):
        if vt.criar_arquivo_pkl():
            st.success("✅ Arquivo .pkl criado/reparado com sucesso!")
            st.rerun()
        else:
            st.error("Falha ao criar/reparar o arquivo .pkl")
    
    # Upload de PDFs
    st.header("📤 Upload de Documentos")
    uploaded_files = st.file_uploader(
        "Arraste PDFs para cá",
        type=["pdf"],
        accept_multiple_files=True
    )
    if uploaded_files:
        for uploaded_file in uploaded_files:
            path = os.path.join(DOCUMENTOS_DIR, uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"{len(uploaded_files)} arquivo(s) salvo(s)!")

    # Processamento dos PDFs
    st.header("⚙️ Processar Documentos")
    if st.button("🔄 Processar Tudo", type="primary"):
        pdfs = [f for f in os.listdir(DOCUMENTOS_DIR) if f.endswith('.pdf')]
        if not pdfs:
            st.warning("Nenhum PDF encontrado!")
        else:
            with st.spinner("Processando..."):
                chunks = []
                processed = set()
                for pdf in pdfs:
                    doc_chunks = processar_pdf(os.path.join(DOCUMENTOS_DIR, pdf))
                    if doc_chunks:
                        chunks.extend(doc_chunks)
                        processed.add(pdf)
                if chunks:
                    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                    vectorstore = FAISS.from_documents(chunks, embeddings)
                    if vt.salvar_memoria(vectorstore, processed):
                        st.success(f"✅ {len(processed)} documentos processados!")
                    else:
                        st.error("Falha ao salvar memória")
                else:
                    st.error("Nenhum conteúdo válido encontrado.")
    
    # Limpar memória
    st.header("🧹 Limpar Memória")
    if st.button("🧹 Limpar Memória", type="secondary"):
        for f in ["index.faiss", "index.pkl"]:
            path = os.path.join(VECTORSTORE_DIR, f)
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(PROCESSED_FILES_PATH):
            os.remove(PROCESSED_FILES_PATH)
        st.success("Memória limpa!")
        st.rerun()

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if st.session_state.logged_in:
        main()
    else:
        login()
