# vectorstore_manager.py

import os
import pickle
import logging
from faiss import read_index
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_DIR = "vectorstore"
PROCESSED_FILES_PATH = "streamlit_app/processed_files.txt"

def verificar_arquivos_memoria():
    """Verifica se os arquivos essenciais do vectorstore existem."""
    required_files = [
        os.path.join(VECTORSTORE_DIR, "index.faiss"),
        os.path.join(VECTORSTORE_DIR, "index.pkl"),
        PROCESSED_FILES_PATH
    ]
    return all(os.path.exists(f) for f in required_files)

def carregar_vectorstore():
    """Carrega o vectorstore local utilizando FAISS."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.load_local(
            folder_path=VECTORSTORE_DIR,
            index_name="index",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        logging.error(f"Erro ao carregar o vectorstore: {e}")
        return None

def criar_arquivo_pkl():
    """Cria ou repara o arquivo .pkl a partir do index.faiss, se necessário."""
    try:
        faiss_path = os.path.join(VECTORSTORE_DIR, "index.faiss")
        pkl_path = os.path.join(VECTORSTORE_DIR, "index.pkl")
        if not os.path.exists(faiss_path):
            raise FileNotFoundError("Arquivo index.faiss não encontrado.")
        index = read_index(faiss_path)
        with open(pkl_path, "wb") as f:
            pickle.dump({
                "docstore": None,
                "index_to_docstore_id": {},
                "faiss_index": index
            }, f)
        return True
    except Exception as e:
        logging.error(f"Erro ao criar/reparar .pkl: {e}")
        return False

def salvar_memoria(vectorstore, processed_files):
    """Salva o vectorstore e a lista de arquivos processados."""
    try:
        vectorstore.save_local(folder_path=VECTORSTORE_DIR, index_name="index")
        # Garante que o .pkl exista
        pkl_path = os.path.join(VECTORSTORE_DIR, "index.pkl")
        if not os.path.exists(pkl_path):
            if not criar_arquivo_pkl():
                raise Exception("Falha ao criar .pkl automaticamente.")
        # Salva a lista de arquivos processados
        with open(PROCESSED_FILES_PATH, 'w') as f:
            for file_name in processed_files:
                f.write(file_name + '\n')
        return True
    except Exception as e:
        logging.error(f"Erro ao salvar a memória: {e}")
        return False
