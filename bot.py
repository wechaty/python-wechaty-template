from __future__ import annotations
import asyncio
from wechaty import Wechaty, WechatyOptions

from dotenv import load_dotenv
from src.plugins.health_checking import HealthCheckingPlugin


if __name__ == "__main__":
    load_dotenv()
    options = WechatyOptions(
        port=8004,
        token="your-token",
        endpoint="127.0.0.1:8083"
    )
    bot = Wechaty(options)
    bot.use([
        HealthCheckingPlugin(),
    ])
    asyncio.run(bot.start())
