from quart import Quart, render_template_string, jsonify
from wechaty import WechatyPlugin

class CounterPlugin(WechatyPlugin):
    # 需要和blueprint注册的UI入口地址一致
    VIEW_URL = '/api/plugins/counter/view'

    def __init__(self):
        # 此方法不能删除
        super().__init__()
        self.count = 0

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/counter/view')
        async def get_counter_view():
            
            with open("./src/plugins/views/table.jinja2", 'r', encoding='utf-8') as f:
            # with open("./src/plugins/views/vue.html", 'r', encoding='utf-8') as f:
                template = f.read()

            self.count += 1
            response = await render_template_string(template, count=self.count)
            return response

class UICounterPlugin(WechatyPlugin):
    # 需要和blueprint注册的UI入口地址一致
    VIEW_URL = '/api/plugins/ui_counter/view'

    def __init__(self):
        # 此方法不能删除
        super().__init__()
        self.count = 0

    async def blueprint(self, app: Quart) -> None:
        
        @app.route('/api/plugins/ui_counter/view')
        async def get_ui_counter_view():
            
            with open("./src/plugins/views/vue.html", 'r', encoding='utf-8') as f:
                template = f.read()
            return template
        
        @app.route('/api/plugins/ui_counter/count')
        async def get_ui_count():
            self.count += 1
            return jsonify({"data": self.count})