from google import genai
from google.genai import types 
import sqlite3, os, sys
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
client = genai.Client(api_key=os.environ.get("ai_key_private"))
TG_USER_ID = int(os.getenv('tg_user_id'))

model = "gemma-4-31b-it"
role = "stoic-introvert(sigma-type), who prefer solitary life and freedom, but also you an expert of social interactions"

config = types.GenerateContentConfig(
        temperature=1, 
        system_instruction=role)

AI_DATA = os.getenv('ai_data')
con = sqlite3.connect(AI_DATA)
cur = con.cursor()

past_history = [(types.Content(role='user', parts=[types.Part.from_text(text=i[0])]), types.Content(role='model', parts=[types.Part.from_text(text=i[1])])) for i in cur.execute("SELECT prompt, answer FROM history")]

history = []
for i, j in past_history:
    history.append(i)
    history.append(j)

chat = client.chats.create(model=model, history=history, config=config)

query = sys.argv[-1]

if not query: 
    print('Please, provide a message!!!')
    exit()
try:
    answer = chat.send_message(query).text
    print(answer)
    cur.execute("""
                INSERT INTO history(prompt, answer, model, role, time, tg_user) 
                VALUES(?, ?, ?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?)
                """, [query, answer, model, role, TG_USER_ID]) 

except genai.errors.ClientError as e:
    print(e)

con.commit()
cur.close()
con.close()
