from config import TOKEN
from apps.handlers import router
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

async def delete_webhook():
    """Удаляем вебхук перед запуском polling"""
    session = AiohttpSession()
    async with Bot(token=TOKEN, session=session) as bot:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Webhook успешно удален")

async def main():
    # 1. Удаляем вебхук перед стартом
    await delete_webhook()
    
    # 2. Инициализируем бота и диспетчер
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # 3. Подключаем роутер
    dp.include_router(router)
    
    # 4. Запускаем polling
    logging.info("Бот запущен в режиме polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")