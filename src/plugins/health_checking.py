"""basic ding-dong bot for the wechaty plugin"""
import asyncio
from typing import Optional
from asyncio import Event
from quart import Quart, jsonify

from wechaty import Message, Wechaty, WechatyPluginOptions
from wechaty.plugin import WechatyPlugin

from wechaty_plugin_contrib.message_controller import message_controller


class HealthCheckingPlugin(WechatyPlugin):
    """health checking plugin"""
    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        super().__init__(options)
        self.event = Event()
        self.is_init = False

    async def init_plugin(self, wechaty: Wechaty) -> None:
        """init the plugin on the dong event"""
        wechaty.on('dong', self.on_dong)

    async def on_dong(self, *args, **kwargs) -> None:
        """listen dong event"""
        if not self.is_init:
            return
        self.event.set()

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        """listen message event"""
        talker = msg.talker()
        text = msg.text()

        if text == 'ding':
            message_controller.disable_all_plugins(msg)
            if msg.room():
                await msg.room().say('dong', mention_ids=[talker.contact_id])
            else:
                await talker.say('dong')

    async def blueprint(self, app: Quart) -> None:
        """add blue print to start web service"""
        @app.route('/ding')
        async def listence_ding():
            if not self.is_init:
                self.event._loop = asyncio.get_event_loop()
                self.is_init = True
            
            await self.bot.puppet.ding()
            if self.event.is_set():
                self.event.clear()
            await self.event.wait()
            self.event.clear()
            return jsonify(dict(code=200, msg='dong'))
