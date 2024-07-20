from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_KEY)

client = OpenAI(
    api_key=OPENAI_KEY,
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)