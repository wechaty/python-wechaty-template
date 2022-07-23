from wechaty import WechatyPlugin, Message
from quart import Quart
from wechaty_plugin_contrib.message_controller import message_controller
from src.ui_plugin import WechatyUIPlugin
from src.utils import SettingFileMixin


class DingDongPlugin(WechatyUIPlugin):

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say("dong")
            message_controller.disable_all_plugins(msg)
    
    def get_nav_info(self):
        return {
            "name": self.name,
            "fetch_url": '/api/plugins/ding_dong/view',
            "icon": "https://wechaty.js.org/img/wechaty-icon.svg"
        }
    
    def get_list_info(self):
        return {
            "name": self.name,
            "author": "wj-Mcat",
            "downloads_count": 1000,
            "icon": "https://wechaty.js.org/img/wechaty-icon.svg",
            "status": 0
        }

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/ding_dong/view')
        def get_ding_dong_view():
            return 'view of ding dong plugin with no UI'
        