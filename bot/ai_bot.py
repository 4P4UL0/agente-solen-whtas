import os
from groq import Groq
from vectorstore_manager import carregar_vectorstore

class AIBot:
    def __init__(self):
        self.model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
        # Carrega o vectorstore usando a função centralizada
        self.vectorstore = carregar_vectorstore()
        if self.vectorstore is None:
            raise FileNotFoundError("Arquivos do vectorstore incompletos ou falha ao carregar. Use o Gerenciador para processar os documentos.")
        
        # Chave da API Groq
        self.groq_api_key = "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"

        if not self.groq_api_key:
            raise ValueError("A chave de API do Groq deve ser fornecida.")
    
    def responder(self, pergunta: str) -> str:
        try:
            # ⚡ Aqui usamos similarity_search_with_score()
            docs_with_scores = self.vectorstore.similarity_search_with_score(pergunta, k=10)
            contexto = "\n\n".join([
                f"**{doc.metadata.get('fonte', 'Fonte desconhecida')} (Score: {score:.2f}):**\n{doc.page_content}"
                for doc, score in docs_with_scores
            ])
            
            client = Groq(api_key=self.groq_api_key)
            
            system_message = f"""Você é um assistente técnico. Baseie-se nestas informações:
{contexto}

Regras:
1. Seja conciso e técnico.
2. Cite a fonte quando relevante.
3. Se não souber, diga "Não encontrado nos documentos".
4. Use markdown para formatação."""
            
            resposta = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.1
            )
            return resposta.choices[0].message.content
        
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
