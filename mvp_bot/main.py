import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database.connection import init_db, close_db
import handlers.start as start
import handlers.quiz as quiz
import handlers.admin as admin


async def on_startup():
    print("🔄 Инициализация базы данных...")
    await init_db()
    print("✅ База данных инициализирована")


async def on_shutdown():
    print("🔄 Закрытие соединений...")
    await close_db()
    print("✅ Соединения закрыты")


async def main():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(start.router, quiz.router, admin.router)

    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
