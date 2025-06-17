# teste_aibot.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.ai_bot import AIBot


def main():
    # Instancia o seu AIBot
    bot = AIBot()
    
    # Simula uma pergunta manual
    pergunta = "Qual é o procedimento de desligamento de equipamento?"
    
    # Chama o método responder
    resposta = bot.responder(pergunta)
    
    print("\nResposta do AIBot:")
    print(resposta)

if __name__ == "__main__":
    main()