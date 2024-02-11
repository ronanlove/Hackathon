from flask import Flask, request, jsonify
from chatbot import chat_with_gpt
app = Flask(__name__)

conversations = []

@app.route('/')
def home():
    return "Welcome to the Chatbot API!"

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get('message')
    
    if 'conversation_id' in data:
        conversation_id = data['conversation_id']
        conversation_id = int(conversation_id) if str(conversation_id).isdigit() else len(conversations)
    else:
        conversation_id = len(conversations)
        conversations.append([])

    if conversation_id >= len(conversations):
        conversations.append([])

    response = chat_with_gpt(user_input)
    
    conversations[conversation_id].extend([
        {"user": user_input, "chatbot": response}
    ])
    
    return jsonify({"response": response, "conversation_id": conversation_id})


@app.route('/retrieve', methods=['GET'])
def retrieve_messages():
    conversation_id = request.args.get('conversation_id', type=int)
    if conversation_id is None or conversation_id >= len(conversations):
        return jsonify({"error": "Invalid conversation ID"}), 400
    
    return jsonify({"conversation": conversations[conversation_id], "conversation_id": conversation_id})

if __name__ == '__main__':
    app.run(debug=True)
