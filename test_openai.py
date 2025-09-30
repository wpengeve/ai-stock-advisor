from dotenv import load_dotenv
import os
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Your OpenAI key is: {api_key}")

# Optional: test a simple call
client = openai.OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or gpt-4 if you have access
    messages=[
        {"role": "user", "content": "Say hi!"}
    ]
)

print(response.choices[0].message.content)