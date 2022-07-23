from typing import Optional
from wechaty import WechatyPlugin, Message, WechatyPluginOptions
from quart import Quart
from wechaty_plugin_contrib.message_controller import message_controller
from src.utils import SettingFileMixin
from src.ui_plugin import WechatyUIPlugin


class RepeaterPlugin(WechatyUIPlugin):

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        talker, room = msg.talker(), msg.room()
        setting = self.get_setting()
        
        conv_id = room.room_id if room else talker.contact_id
        
        if conv_id not in setting.get('admin_ids', []):
            return
        
        await msg.forward(talker)
        message_controller.disable_all_plugins()