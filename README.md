# Architecture
- The project is split into two distinct layers:
    - The Brain (aibot.py): A command-line utility that handles Gemini API communication, enforces personality instructions, and manages conversation state via a local SQLite database.
    - The Gateway (tg_aibot.py): A robust Telethon-based listener that acts as a secure bridge, routing messages from your Telegram client to the engine and relaying responses.

# Key Features
- Persistent Memory: Conversations are stored in SQLite, allowing the AI to "remember" previous interactions across sessions.
- Personality-Driven: Configured with a "Stoic/Sigma" persona, providing concise, expert-level social and strategic advice. Also you can change role for whatever you wish. Just hardcode it 
    ```python
    role = "TYPE ROLE FOR AI ON YOU OWN WISH ..."

- Secure & Private: The gateway is strictly filtered to respond only to your TG_USER_ID, ensuring the bot is personal and private.
- Decoupled Design: The AI engine operates as an independent CLI tool, making it easy to swap the interface or upgrade the engine without modifying the bot code.

# Configuration and usage
1. **Create a .env file in the root directory with the following variables:**
    ```bash
    AI_KEY_PRIVATE=your_gemini_api_key
    AI_DATA=path/to/your/history.db
    AI_PATH=path/to/ai_engine.py
    PRIVATE_APP_ID=your_api_id
    PRIVATE_APP_HASH=your_api_hash
    TG_AIBOT_TOKEN=your_bot_token
    TG_AIBOT_SESSION=bot_session_name
    TG_USER_ID=your_telegram_id

2. **Setup the Database: Ensure you have `ai_data_template.db`, use it for you storing conversation history with AI.**
    
3. **Install Requirements:**
    ```bash
    pip install telethon google-generativeai python-dotenv

4. **Run the Gateway:**
    ```bash
    python tg_aibot.py
