from wechaty import WechatyPlugin, Message
from wechaty_plugin_contrib.message_controller import message_controller

class DingDongPlugin(WechatyPlugin):

    @message_controller
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say("dong")
            message_controller.disable_all_plugins(msg)
