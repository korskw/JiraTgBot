# JiraTgBot
A Telegram bot that monitors new tasks in a Jira project and notifies users when a new issue is created by a specific reporter.

## Features
- Periodically checks for new issues in Jira.
- Sends notifications about new issues via Telegram.
- Allows users to check the last reported tasks.
- Provides status updates on the bot's operation.

## Requirements
- Python 3.8+
- Telegram bot token
- Jira credentials (username & password)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/jira-telegram-bot.git
   cd jira-telegram-bot
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure environment variables in `config.py`:
   ```python
   TELEGRAM_TOKEN = "your-telegram-bot-token"
   JIRA_URL = "https://your-jira-instance.com"
   JIRA_USER = "your-jira-username"
   JIRA_PASSWORD = "your-jira-password"
   JIRA_PROJECT_KEY = "your-jira-project-key"
   JIRA_REPORTER = "reporter-username"
   CHAT_ID = "your-telegram-chat-id"
   ```

## Usage

1. Run the bot:
   ```sh
   python bot.py
   ```

2. Available commands:
   - `/start` – Start the bot and receive a welcome message.
   - `/status` – Check if the bot is running.
   - `/last_tasks` – Retrieve the latest tasks created by the specified reporter.

## How It Works
- The bot continuously monitors Jira for new tasks created by the specified reporter.
- If a new issue is found, it sends a notification to the specified Telegram chat.
- Users can manually request recent tasks using the `/last_tasks` command.
