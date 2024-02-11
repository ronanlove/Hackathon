from flask import Flask, request, jsonify
from chatbot import chat_with_gpt, start_new_conversation
app = Flask(__name__)

conversations = {}

@app.route('/')
def home():
    return "Welcome to the Chatbot API!"

@app.route('/start', methods=['GET'])
def start_conversation():
    conversation_id = start_new_conversation()
    conversations[conversation_id] = {"messages": []}
    return jsonify({"message": "Conversation started", "conversation_id": conversation_id})

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get('message')
    conversation_id = data.get('conversation_id')

    if conversation_id is None or conversation_id not in conversations:
        return jsonify({"error": "Invalid or missing conversation ID"}), 400

    response = chat_with_gpt(user_input, conversation_id)
    
    conversations[conversation_id]["messages"].append({"user": user_input, "chatbot": response})
    
    return jsonify({"response": response, "conversation_id": conversation_id})

@app.route('/retrieve', methods=['GET'])
def retrieve_messages():
    conversation_id = request.args.get('conversation_id', default=None, type=int)
    if conversation_id is None or conversation_id not in conversations:
        return jsonify({"error": "Invalid conversation ID"}), 400
    
    conversation_history = conversations[conversation_id]["messages"]
    return jsonify({"conversation": conversation_history, "conversation_id": conversation_id})

if __name__ == '__main__':
    app.run(debug=True)
