# Architecture
- The project is split into two distinct layers:
    - The Brain `aibot.py`: A command-line utility that handles Gemini API communication, enforces personality instructions, and manages conversation state via a local SQLite database.
    - The Gateway `tg_aibot.py`: A robust Telethon-based listener that acts as a secure bridge, routing messages from your Telegram client to the engine and relaying responses.

# Key Features
- Persistent Memory: Conversations are stored in SQLite, allowing the AI to "remember" previous interactions across sessions.
- Personality-Driven: Configured with a "Stoic/Sigma" persona, providing concise, expert-level social and strategic advice. Also you can change role for whatever you wish. Just hardcode it 
    ```python
    role = "TYPE ROLE FOR AI ON YOU OWN WISH ..."
    ```
- List of models that can generate text:
    ```python
    model = "gemini-3.1-flash-lite" # use model from list below
    ```
    ```bash
    gemini-2.5-flash
    gemini-2.5-pro
    gemini-2.0-flash
    gemini-2.0-flash-001
    gemini-2.0-flash-lite-001
    gemini-2.0-flash-lite
    gemini-2.5-flash-preview-tts
    gemini-2.5-pro-preview-tts
    gemma-4-26b-a4b-it
    gemma-4-31b-it
    gemini-flash-latest
    gemini-flash-lite-latest
    gemini-pro-latest
    gemini-2.5-flash-lite
    gemini-2.5-flash-image
    gemini-3-pro-preview
    gemini-3-flash-preview
    gemini-3.1-pro-preview
    gemini-3.1-pro-preview-customtools
    gemini-3.1-flash-lite-preview
    gemini-3.1-flash-lite
    gemini-3-pro-image-preview
    nano-banana-pro-preview
    gemini-3.1-flash-image-preview
    gemini-3.5-flash
    lyria-3-clip-preview
    lyria-3-pro-preview
    gemini-3.1-flash-tts-preview
    gemini-robotics-er-1.5-preview
    gemini-robotics-er-1.6-preview
    gemini-2.5-computer-use-preview-10-2025
    antigravity-preview-05-2026
    deep-research-max-preview-04-2026
    deep-research-preview-04-2026
    deep-research-pro-preview-12-2025
    ```
 
    
- Secure & Private: The gateway is strictly filtered to respond only to your TG_USER_ID, ensuring the bot is personal and private.
- Decoupled Design: The AI engine operates as an independent CLI tool, making it easy to swap the interface or upgrade the engine without modifying the bot code.

# Configuration and usage
1. **Clone the repo**
    ```bash
    git clone https://github.com/Mister-None/ai
    ```
2. **Install Dependencies:**
    ```bash
    pip install telethon google-generativeai python-dotenv
    ```
3. **Create a `.env` file in the desired directory with the following variables:**
    ```env
    ai_key_private=your_gemini_api_key
    ai_data=path/to/your/history.db
    ai_path=path/to/ai_engine.py
    private_app_id=your_tg_app_id
    private_app_hash=your_tg_app_hash
    tg_aibot_token=your_tg_bot_token
    tg_aibot_session=your_tg_bot_session_name
    tg_user_id=your_telegram_id
    ```
4. **Make permanent variable by exporting `DOTENV_FILE_PATH` in `.bashrc`, etc.**
    ```.bashrc
    export DOTENV_FILE_PATH=path/to/.env
     ```
5. **Setup the Database: Ensure you have `ai_data_template.db`, use it for storing conversation history with AI.**
    
6. **Run the Gateway:**
    ```bash
    python tg_aibot.py
    ```

