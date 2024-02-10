from openai import OpenAI
import random

client = OpenAI(api_key="API_KEY_HERE")



# Example health scenarios
health_scenarios = [
    {"condition": "asthma", "initial_symptom": "shortness of breath and wheezing after exercise"},
    {"condition": "diabetes", "initial_symptom": "increased thirst and frequent urination"},
    {"condition": "mononucleosis", "initial_symptom": "fatigue, sore throat, and fever"},
]

# Initialize a scenario at the start of each session
current_scenario = random.choice(health_scenarios)

def chat_with_gpt(user_input):
    global current_scenario
    prompt = f"You are a patient with {current_scenario['condition']}. Initially, you only mention '{current_scenario['initial_symptom']}'. As the healthcare professional asks more questions, you reveal more details about your condition based on their inquiries. Your age can vary from ages 5-90 years old."
    
    response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Chatbot: Hello Doctor.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)