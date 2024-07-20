from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def formatIntoMarkdown(data):
  client = OpenAI(
      api_key=OPENAI_KEY,
  )

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": f'Here is an array of data: {data}'},
      {"role": "user", "content": f'Organize this data into a markdown file such that no info is lost and personalize the message '}
    ]
  )

  print(completion.choices[0].message)
