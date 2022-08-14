from wechaty import WechatyPlugin
from src.schema import NavMetadata
from src.utils import SettingFileMixin

class WechatyUIPlugin(WechatyPlugin, SettingFileMixin):
    AUTHOR = "wj-mcat"
    AVATAR = 'https://avatars.githubusercontent.com/u/10242208?v=4'
    AUTHOR_LINK = "https://github.com/wj-Mcat"
    ICON = "https://wechaty.js.org/img/wechaty-icon.svg"
    VIEW_URL = None
    UI_DIR = "ui/dist"

    def metadata(self) -> NavMetadata:
        """get the default nav metadata

        Returns:
            NavMetadata: the instance of metadata
        """
        return NavMetadata(
            author=self.AUTHOR,
            author_link=self.AUTHOR_LINK,
            icon=self.ICON,
            avatar=self.AVATAR,
            view_url=self.VIEW_URL
        )