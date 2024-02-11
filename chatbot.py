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

current_scenario = random.choice(health_scenarios)
current_scenario['name'], current_scenario['age'] = generate_personal_info()

conversation_history = []

def chat_with_gpt(user_input):
    global current_scenario, conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    
    if "your name" in user_input.lower():
        return f"My name is {current_scenario['name']}."
    elif "how old are you" in user_input.lower():
        return f"I am {current_scenario['age']} years old."
    
    messages = conversation_history + [{"role": "system", "content": f"You are a patient named {current_scenario['name']} who is {current_scenario['age']} years old with {current_scenario['condition']}. Your initial symptom is '{current_scenario['initial_symptom']}'. You will respond to questions with information relevant to your condition as if you are explaining your symptoms to a healthcare professional for the first time."}]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    response_text = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": response_text})
    
    return response_text

if __name__ == "__main__":
    print("Chatbot: Hello, I'm here to help you practice. What would you like to know?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat_with_gpt(user_input)
        print(f"Chatbot: {response}")