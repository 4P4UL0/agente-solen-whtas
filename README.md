📚 AGENTE SOLEN WHTAS
Assistente Virtual Inteligente que responde perguntas sobre documentos internos via WhatsApp e WebApp, utilizando Vetorização FAISS e Modelos LLM da Groq.

🚀 Sobre o Projeto
Este sistema foi desenvolvido para:
Responder dúvidas automaticamente baseadas em documentos internos (ex: manuais, políticas, treinamentos).
Gerenciar documentos de forma prática via WebApp seguro.
Integrar com WhatsApp usando a API WAHA.
Armazenar conhecimento vetorizado localmente usando FAISS.
Utilizar modelos LLM avançados da Groq para geração de respostas.

🛠️ Tecnologias Usadas
Python 3.12
Flask (API para Webhook WhatsApp)
Streamlit (WebApp para usuários e administradores)
FAISS (Armazenamento de vetores semânticos)
HuggingFace (all-MiniLM-L6-v2 para embeddings)
Groq API (qwen-2.5-coder-32b como modelo LLM)
Docker e Docker Compose (orquestração de containers)
Supervisor (Gerenciamento de múltiplos processos)

📂 Estrutura de Pastas
AGENTE SOLEN WHTAS/
│
├── bot/
│   └── ai_bot.py               # Motor de respostas automáticas
│
├── services/
│   └── waha.py                 # Cliente para comunicação com a API WAHA
│
├── streamlit_app/
│   ├── memoria_manager.py      # App para gerenciar e vetorar documentos (admin)
│   ├── webapp.py               # App público para consultar documentos
│   ├── documentos/             # PDFs carregados para o sistema
│   └── processed_files.txt     # Lista de PDFs já processados
│
├── vectorstore/
│   ├── index.faiss             # Base de dados vetorizada FAISS
│   └── index.pkl               # Metadados do índice FAISS
│
├── api.py                      # Webhook do WhatsApp (Flask)
├── docker-compose.yml          # Orquestração de todos os serviços
├── supervisord.conf            # Gerenciador de processos
├── vectorstore_manager.py      # Utilitário para carregar e salvar a memória
├── .env                        # Arquivo de variáveis de ambiente (API Key Groq)
└── README.md                   # (Este arquivo)

⚙️ Instalação
1. Clone o repositório
git clone https://github.com/seu-usuario/agente-solen-whtas.git
cd agente-solen-whtas

2. Configure o arquivo .env
Crie um arquivo .env com:
GROQ_API_KEY=gsk_seu_token_aqui
(Essa é sua chave pessoal da API da Groq.)

3. (Opcional) Adicione os números autorizados no waha.py
python
Copiar
Editar
autorizados = {
    "seu_numero@c.us",
    "outro_numero@c.us"
}
4. Suba o projeto com Docker
docker-compose up --build

5. Acesse no navegador
Serviço	URL
WebApp Gerenciador de Memória (admin)	http://localhost:8502
WebApp Assistente de Documentos (público)	http://localhost:8501
WhatsApp Webhook (interno)	http://localhost:5000

🧩 Como Funciona
📩 WhatsApp Webhook (API Flask)
O WAHA envia eventos de mensagem recebida para o Flask API (api.py).
O bot verifica se o número é autorizado.
Se autorizado, busca a resposta nos documentos (vectorstore) e responde usando a Groq API.

🛠️ WebApp Gerenciador de Memória (Admin)
Upload de PDFs.
Divisão dos textos em chunks vetorizados.
Geração/Correção do índice FAISS.
Limpeza de memória.

🔐 Protegido com senha (boom@2025).

📚 WebApp Público (Consulta de Documentos)
Permite qualquer usuário buscar respostas em linguagem natural.
Utiliza similaridade vetorial para buscar nos documentos.
Responde de forma formatada em Markdown.

🔒 Segurança
Proteção de Admin: Apenas com senha é possível alterar documentos.
Restrições de WhatsApp: Apenas números autorizados podem conversar com o bot.
Armazenamento Seguro: .env com chave privada não incluído no repositório.

🚀 Deploy em Produção
Para produção, recomenda-se:
Configurar domínio HTTPS reverso (ex: Nginx + Certbot).
Criar um docker-compose.prod.yml otimizando o ambiente.
Usar serviços de monitoramento/logs externos.

🧠 Próximas Melhorias
🔐 Melhorar a autenticação usando tokens JWT para APIs.
📝 Dashboard Admin mostrando estatísticas de perguntas.
📦 Empacotar como pacote Python para fácil instalação.
💬 Incluir suporte para múltiplos idiomas.

👨‍💻 Desenvolvido e alimentado por
Antônio Oliveira | Toni
[antoniospaul6@gmail.com]
[[meu linkedin](https://www.linkedin.com/in/a-paulo/)]
