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
    
    conversation_id = data.get('conversation_id', len(conversations))
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
