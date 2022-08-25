import json
import os
from quart import jsonify
import socket


def get_unused_localhost_port():
    sock = socket.socket()
    # This tells the OS to give us any free port in the range [1024 - 65535]
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def remove_at_info(text: str) -> str:
    """get the clear message, remove the command prefix and at"""
    split_chars = ['\u2005', '\u0020']
    while text.startswith('@'):
        text = text.strip()
        for char in split_chars:
            tokens = text.split(char)
            if len(tokens) > 1:
                tokens = [token for token in text.split(char) if not token.startswith('@')]
                text = char.join(tokens)
            else:
                text = ''.join(tokens)
    return text


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
