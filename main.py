import telebot
import os
import sys
import subprocess
from loguru import logger
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

logger.remove()
logger.add(sys.stderr, format="[<level>{level}</level>] {message}", level="INFO", colorize=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send a Spotify track or album link.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        link = message.text
        bot.reply_to(message, f"Downloading: {link}")

        download_path = "songs/"
        os.makedirs(download_path, exist_ok=True)

        process = subprocess.run([
            "spotdl", link, "--output", download_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode == 0:
            output = process.stdout.decode("utf-8")
            logger.info(output)

            downloaded_files = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]
            if downloaded_files:
                bot.reply_to(message, "Download completed. Sending files...")
                for file_name in downloaded_files:
                    file_path = os.path.join(download_path, file_name)
                    with open(file_path, 'rb') as file:
                        bot.send_document(message.chat.id, file)
                    os.remove(file_path)
            else:
                bot.reply_to(message, "No files found after downloading.")
        else:
            error_message = process.stderr.decode("utf-8")
            logger.error(f"Download error: {error_message}")
            bot.reply_to(message, f"Download error: {error_message}")

    except Exception as e:
        logger.error(f"Processing error: {e}")
        bot.reply_to(message, f"An error occurred: {e}")

if __name__ == '__main__':
    logger.info("Bot is running")
    bot.infinity_polling()
