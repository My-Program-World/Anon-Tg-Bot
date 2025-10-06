import asyncio

from istance import bot, dp


async def main() -> None:
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())