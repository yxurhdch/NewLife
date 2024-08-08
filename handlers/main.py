import logging
import asyncio


from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, loyality, limits


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.rt,
        loyality.rt,
        limits.rt,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
