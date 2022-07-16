
from wechaty import WechatyPlugin
from quart import Quart, request
from src.utils import error, success


class PluginManagerPlugin(WechatyPlugin):

    async def blueprint(self, app: Quart) -> None:
        @app.route('/plugins/nav')
        async def get_plugins_nav():
            plugins = self.bot._plugin_manager._plugins 
            metadata = []
            for name, plugin in plugins.items():
                if hasattr(plugin, "get_nav_info"):
                    metadata.append(plugin.get_nav_info())
            return success(metadata)

        @app.route('/plugins/list')
        async def get_plugin_list():
            plugins = self.bot._plugin_manager._plugins
            
            plugin_list = []
            for name, plugin in plugins.items():
                if hasattr(plugin, "get_list_info"):
                    info =  plugin.get_list_info()
                    status = self.bot._plugin_manager.plugin_status(name)
                    info['status'] = status.name
                    plugin_list.append(info)

            return success(plugin_list)

        @app.route('/plugins/status', methods=['PUT'])
        async def change_status():
            data = await request.get_json()
            name = data.get('plugin_name', None) 
            status = data.get('status', None)
            if status == 'Stopped':
                await self.bot._plugin_manager.stop_plugin(name)
            elif status == 'Running':
                await self.bot._plugin_manager.start_plugin(name)
            else:
                return error("unexpected plugin status, which should be one of<Stopped, Running>")
            return success('changes success ...')
        