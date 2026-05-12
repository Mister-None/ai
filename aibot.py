from google import genai
from google.genai import types
from colorama import Fore, Style, init
import os
import base64
from dotenv import load_dotenv
init(autoreset=True)
load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
client = genai.Client(api_key=os.environ.get("ai_key"))
model = "gemini-flash-lite-latest"
tools = [types.Tool(googleSearch=types.GoogleSearch()),]
generate_content_config = types.GenerateContentConfig(tools=tools, temperature=0.5)#, system_instruction="You are a crypto trader, who prefer stable income, also you know python and prefer do things concise")
chat_history = []
while True:
    query = input(Fore.CYAN+'>>> ')
    if query == 'quit': break
    chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=query)]))
    try:
        full_response = ""
        print(Fore.GREEN + Style.BRIGHT, end="")
        for chunk in client.models.generate_content_stream(model=model, contents=chat_history, config=generate_content_config,):
            if chunk.text:
                print(chunk.text, end="")
                full_response += chunk.text
        chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=full_response)]))
    except genai.errors.ClientError as e:
        print(Fore.RED + str(e))
        for model in client.models.list():
           # if 'gemini' in model.name:
            print(Fore.YELLOW + model.name)
        exit()
