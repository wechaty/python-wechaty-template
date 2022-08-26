import asyncio
from wechaty import WechatyPlugin, Message
from quart import Quart, render_template_string, request
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty import WechatyPlugin
from src.utils import success, error

class SendMessagePlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/send_messages/view'

    def __init__(self, options = None):
        super().__init__(options)
        
        self.sleep_second: int = 1

    async def blueprint(self, app: Quart) -> None:

        @app.route("/api/plugins/send_message/text/<content>")
        async def send_text_message_to_admin(content: str):
            admin_id = self.setting.get('admin_id', None)
            if admin_id is None:
                return "not admin id"
            contact = self.bot.Contact.load(admin_id)
            await contact.say(content)
            return "success"

        @app.route("/api/plugins/send_message/room", methods=['POST'])
        async def send_text_message_to_rooms():
            data = await request.get_json()
            room_ids = data.get("room_ids", [])
            text = data.get("text", '')
            
            if not room_ids or not text:
                return error('not valid messages')
            
            for room_id in room_ids:
                room = self.bot.Room.load(room_id)
                await room.say(text)
                await asyncio.sleep(self.sleep_second)
            
            return success("success")

        @app.route(SendMessagePlugin.VIEW_URL)
        async def send_message_view():
            with open("./src/plugins/views/send_message.html", 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        
        @app.route('/api/plugins/send_message/room_select')
        async def get_room_select():
            room_select = []
            rooms = await self.bot.Room.find_all()
            for room in rooms:
                if not room.payload.topic or not room.room_id:
                    continue
                room_select.append(dict(
                    value=room.room_id,
                    label=room.payload.topic
                ))
            
            return success(room_select)
