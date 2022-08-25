from quart import Quart, render_template_string, jsonify
from wechaty import WechatyPlugin


class ChatHistoryPlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/chat_history/view'

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/counter/view')
        async def get_counter_view():
            
            with open("./src/plugins/views/table.jinja2", 'r', encoding='utf-8') as f:
            # with open("./src/plugins/views/vue.html", 'r', encoding='utf-8') as f:
                template = f.read()
            
            self.setting['count'] += 1

            response = await render_template_string(template, count=self.setting['count'])
            return response