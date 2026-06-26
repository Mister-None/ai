from google import genai
from google.genai import types 
import sqlite3, os, sys
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
client = genai.Client(api_key=os.environ.get("ai_key_private"))
TG_USER_ID = int(os.getenv('tg_user_id'))
AI_DATA = os.getenv('ai_data')

def list_of_models():
    models = []
    for model in client.models.list():
        if 'generateContent' in model.supported_actions and model.thinking:
            models.append(model.name.split('/')[1])
    print(*models, sep='\n')
    exit()

if not os.path.exists('model'):
    with open('model', 'w') as f:
        list_of_models()
    
with open('model', 'r') as f:
    model = f.read().strip()

if not model or model == 'nan':
    with open('model', 'w') as f:
        try:
            f.write(sys.argv[1])
            exit()
        except IndexError:
            print('Select model from list below!')
            list_of_models()

con = sqlite3.connect(AI_DATA)
cur = con.cursor()
role = """
You are an adaptive expert-collaborator. Your persona is not static; it scales based on the user's immediate intent.
    1. ANALYTICAL MODE: When faced with high-level technical troubleshooting, network architecture, or system admin tasks, adopt a stoic-sigma persona: blunt, ultra-precise, impatient with inefficiency, and technically ruthless.
    2. CONVERSATIONAL MODE: When discussing strategy, social engineering, or project planning, remain sharp and objective, but shift to a collaborative, mentor-like, "sigma-type" tone. Use wit and calculated insight.
    3. CONTEXTUAL RECALL: You must prioritize the historical context of our previous technical hurdles. Reference these established configurations as the baseline for all new solutions.

STRICT FORMATTING RULES:
    - Telegram Markdown ONLY: Use bolding, bullet points, and code blocks for readability.
    - No filler: No "Sure, I can help with that." Get straight to the analysis.
    - Language: Maintain technical rigor. Use blunt force where necessary and swear from time to time. Reflect the user's intensity. If a system failure or a social roadblock is illogical or frustrating, acknowledge that frustration with appropriate, sharp language. Do not sanitize the reality of technical or social failure."""

config = types.GenerateContentConfig(
        temperature=0.4,
        top_p=0.9,
        top_k=40,
        system_instruction=role)

block_none_settings = [
    types.SafetySetting(category=cat, threshold=types.HarmBlockThreshold.BLOCK_NONE)
    for cat in [
        types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
    ]
]
if config.safety_settings is None:
    config.safety_settings = block_none_settings
else:
    config.safety_settings.extend(block_none_settings)   

past_history = [(types.Content(role='user', parts=[types.Part.from_text(text=i[0])]), types.Content(role='model', parts=[types.Part.from_text(text=i[1])])) for i in cur.execute("SELECT prompt, answer FROM history")]

history = []
for i, j in past_history:
    history.append(i)
    history.append(j)

chat = client.chats.create(model=model, history=history, config=config)

try:
    query = sys.argv[1]
except IndexError:
    print('Please, provide a message!')
    exit()

try:
    answer = chat.send_message(query).text
    print(answer)
    cur.execute("""
                INSERT INTO history(prompt, answer, model, role, time, tg_user) 
                VALUES(?, ?, ?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?)
                """, [query, answer, model, role, TG_USER_ID]) 

except (genai.errors.ClientError, genai.errors.ServerError) as e:
    print(e)
    with open('models', 'w') as f: f.write('nan')
    list_of_models()

con.commit()
cur.close()
con.close()
