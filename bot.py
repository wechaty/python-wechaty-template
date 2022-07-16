"""template of your bot"""
from __future__ import annotations
import asyncio
from wechaty import Wechaty, WechatyOptions

from dotenv import load_dotenv
from src.plugins.plugin_manager import PluginManagerPlugin
from src.plugins.ding_dong import DingDongPlugin
from src.plugins.repeater import RepeaterPlugin


if __name__ == "__main__":
    load_dotenv()
    options = WechatyOptions(
        port=8004,
    )
    bot = Wechaty(options)
    bot.use([
        PluginManagerPlugin(),
        DingDongPlugin(),
        RepeaterPlugin()
    ])
    asyncio.run(bot.start())
