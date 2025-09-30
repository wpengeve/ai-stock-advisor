import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def call_gpt_with_retries(prompt, model="gpt-4", temperature=0.7, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return f"❌ GPT failed to respond after {retries} attempts.\n\nError: {e}"