# api.py

from flask import Flask, request, jsonify
from services.waha import Waha
from bot.ai_bot import AIBot

app = Flask(__name__)

ai_bot = AIBot()
waha = Waha()

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    print(f'EVENTO RECEBIDO: {data}')
    
    chat_id = data['payload']['from']
    message_body = data['payload']['_data']['body']
    name = data['payload']['_data']['notifyName']
    
    is_group = '@g.us' in chat_id
    is_status = 'status@broadcast' in chat_id
    
    if is_group or is_status:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'}), 200
    
    aut = waha.seg(chat_id)
    
    waha.start_typing(chat_id=chat_id)
        
    if aut != "aut":
        message = (
            f'Olá, {name}! Tudo bem?\n\nMeu nome é Solen e sou assistente virtual. '
            "No momento, não tenho autorização para lhe responder.\n\n"
            "Por favor, entre em contato com a Gerência para que eles possam liberar o acesso. "
            "Agradeço a compreensão! 😊"
        )
    else:
        if ai_bot is None:
            message = "Erro na inicialização do assistente de documentos. Por favor, contate o administrador."
        else:
            message = ai_bot.responder(message_body)
   
    waha.send_message(chat_id=chat_id, message=message)
    waha.stop_typing(chat_id=chat_id)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
