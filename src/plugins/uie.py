from typing import Optional
from wechaty import WechatyPlugin, Message, Room
from quart import Quart, render_template_string
from wechaty_plugin_contrib.message_controller import message_controller

from wechaty import WechatyPlugin
from src.utils import remove_at_info
from paddlenlp import Taskflow
from pprint import pformat, pprint

from tap import Tap


class UIEParams(Tap):
    schema: Optional[str] = None
    text: Optional[str] = None

class Predictor:
    
    uie_model = None

    @staticmethod
    def predict(text) -> str:
        if Predictor.uie_model is None:
            ie = Taskflow('information_extraction', schema=['时间', '地点', '人物', '公司'])
            result = pformat(ie(params.text))


class UIEPlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/uie/view'

    def __init__(self):
        super().__init__()

        self.prefix = 'task_flow.uie'

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        room = msg.room()
        text = msg.text()

        if self.prefix not in text:
            return
        
        if room is not None:
            if not await msg.mention_self():
                return
            text = remove_at_info(text).strip()
        
        if not text.startswith(self.prefix):
            return None
        
        # parse the arguments
        args = text.split()
        params: UIEParams = UIEParams().parse_args(args, known_only=True)
        
        if params.schema is None or params.text is None:
            return None
        
        schema = eval(params.schema)
        ie = Taskflow('information_extraction', schema=schema)
        
        result = pformat(ie(params.text))

        if room:
            await room.say(result, mention_ids=[msg.talker().contact_id])
        else:
            await msg.say(str(result))