"""template of your bot"""
from __future__ import annotations
import asyncio
from wechaty import Wechaty, WechatyOptions

from dotenv import load_dotenv
from src.plugins.health_checking import HealthCheckingPlugin
from src.plugins.tts import TTSPlugin


if __name__ == "__main__":
    load_dotenv()
    options = WechatyOptions(
        # port of web service
        port=8004,
    )
    bot = Wechaty(options)
    bot.use([
        # HealthCheckingPlugin(),
        TTSPlugin()
    ])
    asyncio.run(bot.start())
