from typing import Optional, List, Dict 
from wechaty import WechatyPlugin
from wechaty.plugin import PluginStatus
from quart import Quart, request
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from src.utils import error, success
from src.schema import NavMetadata
from src.ui_plugin import WechatyUIPlugin

@dataclass_json
@dataclass
class NavDTO:
    name: str                       # name of plugin
    status: int                     # status of plugin: 0 / 1
    
    view_url: Optional[str] = None 
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author
    
    def update_metadata(self, nav_metadata: NavMetadata):
        self.author = nav_metadata.author
        self.author_link = nav_metadata.author_link
        self.avatar = nav_metadata.avatar
        self.icon = nav_metadata.icon
        self.view_url = nav_metadata.view_url


class PluginManagerPlugin(WechatyPlugin):
    IS_SYSTEM_PLUGIN = True
    async def blueprint(self, app: Quart) -> None:

        @app.route('/plugins/list')
        async def get_plugins_nav():
            plugins: Dict[str, WechatyUIPlugin] = self.bot._plugin_manager._plugins

            navs: List[NavDTO] = []
            for name, plugin in plugins.items():
                if getattr(plugin, 'IS_SYSTEM_PLUGIN', None) == True:
                    continue
                nav = NavDTO(
                    name=name,
                    status=int(
                        self.bot._plugin_manager._plugin_status[name] == PluginStatus.Running
                    ))
                nav.update_metadata(
                    plugin.metadata()
                )
                navs.append(nav.to_dict())
            return success(navs)

        @app.route('/plugins/status', methods=["POST", 'PUT'])
        async def change_status():
            data = await request.get_json()
            name = data.get('plugin_name', None)
            status = data.get('status', None)
            if not name or not status:
                return error('the plugin_name and status field is required ...')
            status = int(status)
            if status == 0:
                await self.bot._plugin_manager.stop_plugin(name)
            elif status == 1:
                await self.bot._plugin_manager.start_plugin(name)
            else:
                return error("unexpected plugin status, which should be one of<Stopped, Running>")
            return success('changes success ...')
        

        @app.route('/plugins/setting', methods=['GET'])
        async def get_plugin_setting():
            name = request.args.get('plugin_name', None)

            plugin: WechatyUIPlugin = self.bot._plugin_manager._plugins.get(name, None)
            if not plugin:
                return error(f'plugin<{name}> not exist ...')
            config_entry = 'get_setting'
            if not hasattr(plugin, config_entry):
                return error(f'this plugin<{name}> contains no setting ...')

            setting = plugin.get_setting()
            return success(setting)

        @app.route('/plugins/setting', methods=['POST'])
        async def update_plugin_setting():
            data = await request.get_json()
            name = data.get('plugin_name', None)

            plugin: WechatyUIPlugin = self.bot._plugin_manager._plugins.get(name, None)
            if not plugin:
                return error(f'plugin<{name}> not exist ...')

            plugin.update_setting(
                data.get('setting', {})
            )
            return success(None)
