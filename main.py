import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from jira import JIRA

import config

TELEGRAM_TOKEN = config.TELEGRAM_TOKEN
JIRA_URL = config.JIRA_URL
JIRA_USER = config.JIRA_USER
JIRA_PASSWORD = config.JIRA_PASSWORD
JIRA_PROJECT_KEY = config.JIRA_PROJECT_KEY
JIRA_REPORTER = config.JIRA_REPORTER
CHAT_ID = config.CHAT_ID

jira_options = {"server": JIRA_URL}
jira = JIRA(options=jira_options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

last_seen_issue = None


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Бот запущен! Ожидаю новые задачи в Jira.")


async def get_status(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Бот работает и мониторит Jira.")


async def check_new_issues():
    global last_seen_issue
    jql_query = f'project={JIRA_PROJECT_KEY} AND reporter="{JIRA_REPORTER}" ORDER BY created DESC'
    issues = jira.search_issues(jql_query, maxResults=5)

    if issues:
        latest_issue = issues[0]
        if last_seen_issue is None:
            last_seen_issue = latest_issue.key

        if latest_issue.key != last_seen_issue:
            message = f"🔔 Новая задача: {latest_issue.key}\n" \
                      f"📌 {latest_issue.fields.summary}\n" \
                      f"🔗 {JIRA_URL}/browse/{latest_issue.key}"
            await send_telegram_message(message)
            last_seen_issue = latest_issue.key


async def send_telegram_message(text):
    from telegram import Bot
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)


async def last_tasks(update: Update, context: CallbackContext) -> None:
    jql_query = f'project={JIRA_PROJECT_KEY} AND reporter="{JIRA_REPORTER}" ORDER BY created DESC'
    issues = jira.search_issues(jql_query, maxResults=5)

    message = "📝 Последние задачи:\n"
    for issue in issues:
        message += f"🔹 [{issue.key}] {issue.fields.summary}\n🔗 {JIRA_URL}/browse/{issue.key}\n"

    await update.message.reply_text(message)


async def periodic_check():
    while True:
        await check_new_issues()  # Проверяем новые задачи
        await asyncio.sleep(5)  # Пауза перед следующей проверкой


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", get_status))
    app.add_handler(CommandHandler("last_tasks", last_tasks))

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_check())

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
