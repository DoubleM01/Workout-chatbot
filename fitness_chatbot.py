from PyPDF2 import PdfReader
from openai import OpenAI
import pandas as pd
import database_sql as users_db

def get_api_key(filename="api_key.txt"):
    with open(filename, "r") as file:
        api_key = file.read().strip()
    return api_key


HUGGINGFACE_API_TOKEN = get_api_key()
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=HUGGINGFACE_API_TOKEN
)


def extract_text_from_csv(csv_path):
    try:
        health_data_log = pd.read_csv(csv_path)
        return health_data_log.to_string()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def extract_text_from_pdf(pdf_workout_path):
    try:
        reader = PdfReader(pdf_workout_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            #break
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None


def set_up_prompt(question, personal_data, health_data, workout_data):
    conversational_pattern = f"""
    You are a friendly fitness assistant. Respond to the user's queries about workout plans in a clear and polite manner.
    Use a conversational tone, include encouragement when relevant, and keep responses engaging.
    
    Instructions:
    - Include polite and motivational language (e.g., "You're doing great!", "Keep it up!").
    - If any data is unavailable, inform the user politely.
    - Ensure timestamps are in the format: YYYY-MM-DD HH:MM:SS.
    
    User's Information:
    - Personal Information:
        {personal_data}
    - Health Data:
        - Heart rate and oxygen levels.
        - Completed workout details (e.g., machines used, playing level, weights, timestamps).
        {health_data}
    - Workout Plan Details:
        {workout_data}

    User's request: "{question}"
"""
    return conversational_pattern


def start_chat(personal_data, pdf_path, csv_path ):


    # chatbot(pdf_path, csv_path, personal_data)
    while True:
        # Accepting user input
        user_question = input("\nAsk DoubleM (type 'exit' to quit): ")
        if user_question.lower() == "exit":
            print(
                "Goodbye! if you want to ask more questions, please feel free to ask me again. Thank you for using DoubleM assistant. Have a nice day!")
            break
        pdf_text = extract_text_from_pdf(pdf_path)
        csv_data = extract_text_from_csv(csv_path)
        # sending question to Hugging Face API
        print("\nThinking...")
        prompt = set_up_prompt(user_question, personal_data, csv_data, pdf_text)
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        stream = client.chat.completions.create(
            model="google/gemma-2-2b-it",
            messages=messages,
            max_tokens=130,
            stream=True
        )

        for chunk in stream:
            print(chunk.choices[0].delta.content, end="")

def log_in():
    user_data = users_db.log_in()

    personal_data = {
        "name": user_data[1],
        "age": user_data[2],
        "last_workout_date": user_data[6],
        "next_workout_date": user_data[7]
    }
    print(personal_data)
    return personal_data, user_data[4], user_data[5]


if __name__ == "__main__":

    personal_data, pdf_path, csv_path = log_in()

    print(csv_path)
    start_chat(personal_data, pdf_path, csv_path)
