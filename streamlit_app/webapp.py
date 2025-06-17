# streamlit_app/webapp.py

import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import logging

# Configurações (fixas)
VECTORSTORE_DIR = "vectorstore"
PROCESSED_FILES_PATH = "streamlit_app/processed_files.txt"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# Logging direto
logging.basicConfig(
    filename="streamlit_app/solem_app.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Página Streamlit
st.set_page_config(
    page_title="Solem - Assistente de Documentos",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def carregar_memoria():
    """Carrega a memória FAISS"""
    try:
        required_files = [
            os.path.join(VECTORSTORE_DIR, "index.faiss"),
            os.path.join(VECTORSTORE_DIR, "index.pkl")
        ]
        if not all(os.path.exists(f) for f in required_files):
            st.error("Arquivos de memória incompletos. Use o Gerenciador primeiro.")
            return None
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.load_local(
            folder_path=VECTORSTORE_DIR,
            index_name="index",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        logging.error(f"Erro ao carregar: {str(e)}")
        st.error(f"Erro crítico: {str(e)}")
        return None

vectorstore = carregar_memoria()
processed_files = set()

if os.path.exists(PROCESSED_FILES_PATH):
    with open(PROCESSED_FILES_PATH, 'r') as f:
        processed_files = set(line.strip() for line in f)

st.title("📚 Solem - Assistente de Documentos")

with st.sidebar:
    st.title("🔍 Status")
    if vectorstore:
        st.success(f"✅ Memória carregada ({len(processed_files)} documentos)")
        with st.expander("Ver documentos"):
            for doc in sorted(processed_files):
                st.write(f"- {doc}")
    else:
        st.error("❌ Memória não carregada")
    
    if st.button("🔄 Atualizar"):
        st.rerun()

def gerar_resposta(pergunta):
    """Gera uma resposta baseada na memória"""
    try:
        docs = vectorstore.similarity_search(pergunta, k=13)
        contexto = "\n\n".join([f"**{doc.metadata['fonte']}:**\n{doc.page_content}" for doc in docs])
        
        client = Groq(api_key="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")
        resposta = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": f"""Você é um assistente técnico. Baseie-se nestas informações:
                    {contexto}

                    Regras:
                    1. Seja conciso e técnico
                    2. Cite a fonte quando relevante
                    3. Se não souber, diga "Não encontrado nos documentos"
                    4. Use markdown para formatação"""
                },
                {"role": "user", "content": pergunta}
            ],
            temperature=0.3
        )
        return resposta.choices[0].message.content
    except Exception as e:
        logging.error(f"Erro na resposta: {str(e)}")
        return f"⚠️ Erro: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre seus documentos..."):
    if not vectorstore:
        st.error("Memória não carregada. Use o Gerenciador primeiro.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Pesquisando..."):
        resposta = gerar_resposta(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
