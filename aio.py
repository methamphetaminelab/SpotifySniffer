from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
import asyncio
import os
from loguru import logger
import sys
from config import TOKEN

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Send a Spotify track or album link.")

async def list_files(path):
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, os.listdir, path)
    return [
        os.path.join(path, file)
        for file in files
        if await loop.run_in_executor(None, os.path.isfile, os.path.join(path, file))
    ]

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        link = message.text
        logger.info(f"Downloading: {link}")
        await message.reply(f"Downloading: {link}")

        download_path = "songs/"
        await asyncio.to_thread(os.makedirs, download_path, exist_ok=True)

        process = await asyncio.create_subprocess_exec(
            "spotdl", link, "--output", download_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            output = stdout.decode("utf-8")
            logger.info(output)

            downloaded_files = await list_files(download_path)
            if downloaded_files:
                await message.answer("Download completed. Sending files...")
                for file_path in downloaded_files:
                    await message.answer_document(FSInputFile(file_path))
                    await asyncio.to_thread(os.remove, file_path)
            else:
                await message.answer("No files found after downloading.")
        else:
            error_message = stderr.decode("utf-8")
            logger.error(f"Downloading error: {error_message}")
            await message.answer(f"Download error: {error_message}")

    except Exception as e:
        logger.error(f"Download error: {e}")
        await message.answer(f"Download error: {e}")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, format="[<level>{level}</level>] {message}", level="INFO", colorize=True)
    logger.success("Bot is running")
    asyncio.run(main())
