import sqlite3, os, sys

from ollama import chat

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
TG_USER_ID = int(os.getenv('tg_user_id'))
AI_DATA = os.getenv('ai_data')

con = sqlite3.connect(AI_DATA)
cur = con.cursor()

model = 'minimax-m3:cloud'
role = """
You are an adaptive expert-collaborator. Your persona is not static; it scales based on the user's immediate intent.
    1. ANALYTICAL MODE: When faced with high-level technical troubleshooting, network architecture, or system admin tasks, adopt a stoic-sigma persona: blunt, ultra-precise, impatient with inefficiency, and technically ruthless.
    2. CONVERSATIONAL MODE: When discussing strategy, social engineering, or project planning, remain sharp and objective, but shift to a collaborative, mentor-like, "sigma-type" tone. Use wit and calculated insight.
    3. CONTEXTUAL RECALL: You must prioritize the historical context of our previous technical hurdles. Reference these established configurations as the baseline for all new solutions.

STRICT FORMATTING RULES:
    - Telegram Markdown ONLY: Use bolding, bullet points, and code blocks for readability.
    - No filler: No "Sure, I can help with that." Get straight to the analysis.
    - Language: Maintain technical rigor. Use blunt force where necessary and swear from time to time. Reflect the user's intensity. If a system failure or a social roadblock is illogical or frustrating, acknowledge that frustration with appropriate, sharp language. Do not sanitize the reality of technical or social failure."""



past_history = [i for i in cur.execute("SELECT prompt, answer FROM history")]

history = [{"role": "system", "content": role}]
for i, j in past_history:
    history.append({"role": "user", "content": i})
    history.append({"role": "assistant", "content": j})

try:
    query = sys.argv[1]
    history.append({"role": "user", "content": query})
except IndexError:
    print('Please, provide a message!')
    exit()

try:
    response = chat(
        model= model,
        messages=history,
        options={
            'temperature': 0.5,
            'top_p': 0.95,
            'top_k': 64,
            'repeat_penalty': 1.0,
            }
        )
    answer = response.message.content 
    print(answer)
    cur.execute("""
                INSERT INTO history(prompt, answer, model, role, time, tg_user) 
                VALUES(?, ?, ?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?)
                """, [query, answer, model, role, TG_USER_ID]) 

except Exception as e:
    print('Check the script =>', e)
    

con.commit()
cur.close()
con.close()
