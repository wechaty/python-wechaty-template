from wechaty import WechatyPlugin, Message
from quart import Quart
from wechaty_plugin_contrib.message_controller import message_controller


class RepeaterPlugin(WechatyPlugin):

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        if msg.room():
            return None
        
        await msg.say(msg)
     
    def get_nav_info(self):
        return {
            "name": self.name,
            "fetch_url": f'/api/plugins/{self.name.lower()}/view',
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

        @app.route(f'/api/plugins/{self.name.lower()}/view')
        def get_repeater_view():
            return 'view of repeater plugin with no UI'