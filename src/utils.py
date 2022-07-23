import json
import os
from quart import jsonify


class SettingFileMixin:

    def get_setting_file(self) -> str:
        if hasattr(self, 'setting_file'):
            return self.setting_file
        self.setting_file = os.path.join(self.cache_dir, 'setting.json')
        os.makedirs(
            os.path.dirname(self.setting_file),
            exist_ok=True
        )
        return self.setting_file

    @property
    def setting(self) -> dict:
        return self.get_setting(force_load=False)
    
    @setting.setter
    def setting(self, value: dict) -> dict:
        self.update_setting(value)

    def get_setting(self, force_load: bool = False) -> dict:
        """get the setting from the file"""
        with open(self.get_setting_file(), 'r', encoding='utf-8') as f:
            setting = json.load(f)
        return setting 
    
    def update_setting(self, setting: dict) -> None: 
        with open(self.get_setting_file(), 'w', encoding='utf-8') as f:
            json.dump(setting, f, ensure_ascii=True)
        return setting


def success(data):
    return jsonify({
        "data": data,
        "code": 200
    })

def error(msg):
    return jsonify({
        "msg": msg,
        "code": 500
    })
