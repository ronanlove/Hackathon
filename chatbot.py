from openai import OpenAI
import random
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Security

health_scenarios =[
    {"condition": "asthma", "initial_symptom": "shortness of breath and wheezing after exercise"},
    {"condition": "diabetes", "initial_symptom": "increased thirst and frequent urination"},
    {"condition": "mononucleosis", "initial_symptom": "fatigue, sore throat, and fever"},
    {"condition": "hypertension", "initial_symptom": "headaches, shortness of breath, and nosebleeds"},
    {"condition": "gastroesophageal reflux disease (GERD)", "initial_symptom": "heartburn, chest pain, and regurgitation of food or sour liquid"},
    {"condition": "anemia", "initial_symptom": "fatigue, pale or yellowish skin, and cold hands and feet"},
    {"condition": "depression", "initial_symptom": "persistent sad, anxious, or empty mood; feelings of hopelessness"},
    {"condition": "anxiety", "initial_symptom": "excessive worry, feeling agitated, and restlessness"},
    {"condition": "migraine", "initial_symptom": "severe headache, nausea, and sensitivity to light and sound"},
    {"condition": "allergic rhinitis", "initial_symptom": "sneezing, itchy nose, and nasal congestion"},
    {"condition": "urinary tract infection (UTI)", "initial_symptom": "burning sensation when urinating and strong, persistent urge to urinate"},
    {"condition": "osteoporosis", "initial_symptom": "back pain, caused by a fractured or collapsed vertebra, and loss of height over time"},
    {"condition": "chronic obstructive pulmonary disease (COPD)", "initial_symptom": "chronic cough, shortness of breath, and frequent respiratory infections"},
    {"condition": "heart attack", "initial_symptom": "chest pain or discomfort, shortness of breath, and nausea or lightheadedness"},
    {"condition": "stroke", "initial_symptom": "sudden numbness or weakness in the face, arm, or leg, especially on one side of the body; confusion; trouble speaking"},
]

def generate_personal_info():
    names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Jamie", "Morgan", "Avery"]
    name = random.choice(names)
    age = random.randint(5, 90)
    return name, age

conversations = {}

def start_new_conversation():
    conversation_id = len(conversations) + 1
    name, age = generate_personal_info()
    scenario = random.choice(health_scenarios)
    initial_prompt = f"You are a patient named {name} who is {age} years old with {scenario['condition']}. Your initial symptom is '{scenario['initial_symptom']}'."
    
    conversations[conversation_id] = {
        "scenario": scenario,
        "name": name,
        "age": age,
        "messages": [{"role": "system", "content": initial_prompt}]
    }
    return conversation_id

def chat_with_gpt(user_input, conversation_id):
    conversation = conversations[conversation_id]
    
    if "your name" in user_input.lower():
        response_text = f"My name is {conversation['name']}."
    elif "how old are you" in user_input.lower():
        response_text = f"I am {conversation['age']} years old."
    else:
        conversation['messages'].append({"role": "user", "content": user_input})
        
        messages = conversation['messages']
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        response_text = response.choices[0].message.content.strip()
        conversation['messages'].append({"role": "assistant", "content": response_text})
    
    return response_text

if __name__ == "__main__":
    print("Chatbot: Hello, I'm here to help you practice. What would you like to know?")
    current_conversation_id = start_new_conversation()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat_with_gpt(user_input, current_conversation_id)
        print(f"Chatbot: {response}")