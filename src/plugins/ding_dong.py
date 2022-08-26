from wechaty import WechatyPlugin, Message
from quart import Quart, render_template_string
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty import WechatyPlugin

class DingDongPlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/ding_dong/view'

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say("dong")
            await msg.say("I'm alive ...")
            message_controller.disable_all_plugins(msg)

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/ding_dong/view')
        async def get_ding_dong_view():
            
            # with open("./src/plugins/views/table.jinja2", 'r', encoding='utf-8') as f:
            with open("./src/plugins/views/vue.html", 'r', encoding='utf-8') as f:
                template = f.read()

            data = [i for i in range(20)]
            response = await render_template_string(template, tables=data)
            return response