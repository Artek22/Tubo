import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config_data.config import load_config
from handlers import user_handlers

logger = logging.getLogger(__name__)

# Загружаем конфиг в переменную config
config = load_config()

# Инициализируем бот и диспетчер
bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)


async def main():
    """Функция конфигурирования и запуска бота."""
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s"
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logger.info('Bot stopped!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped!')