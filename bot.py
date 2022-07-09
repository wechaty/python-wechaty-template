import asyncio
import sys
from wechaty import Wechaty, WechatyOptions

from dotenv import load_dotenv
from plugins.ding_dong import DingDongPlugin


async def final_failure_handler(*args, **kwargs):
    sys.exit()


if __name__ == "__main__":
    load_dotenv()
    options = WechatyOptions(
        port=8004,
        token="your-token",
        endpoint="127.0.0.1:8083"
    )
    bot = Wechaty(options)
    bot.use([
        DingDongPlugin(),
    ])
    asyncio.run(bot.start())