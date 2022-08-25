"""template of your bot"""
from __future__ import annotations
import asyncio
import os
from wechaty import Wechaty, WechatyOptions

from dotenv import load_dotenv
from wechaty_plugin_contrib.contrib.info_logger import InfoLoggerPlugin
from src.plugins.ding_dong import DingDongPlugin
from src.plugins.repeater import RepeaterPlugin
from src.plugins.counter import CounterPlugin, UICounterPlugin
from src.plugins.github_message_forwarder import GithubMessageForwarderPlugin


if __name__ == "__main__":
    load_dotenv()
    options = WechatyOptions(
        port=os.environ.get('port', 8004)
    )
    bot = Wechaty(options)
    bot.use([
        DingDongPlugin(),
        RepeaterPlugin(),
        InfoLoggerPlugin(),
        CounterPlugin(),
        UICounterPlugin(),
        GithubMessageForwarderPlugin(
            endpoint=os.environ.get('github_endpoint', None) or "your-custom-endpoint"
        ),
    ])
    asyncio.run(bot.start())
