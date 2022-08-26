""""""
from collections import defaultdict
import os
import re
from typing import (
    Dict, Optional, List, Set, Tuple, Union
)
from dataclasses import dataclass
from wechaty import (
    Contact,
    FileBox,
    MessageType,
    WechatyPlugin,
    Room,
    Message,
    WechatyPluginOptions
)
from wechaty_puppet import get_logger

from src.utils import remove_at_info
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty_puppet.schemas.base import BaseDataClass


@dataclass
class Conversation(BaseDataClass):
    """Room or Contact Configuraiton"""
    alias: str
    id: str
    type: str = 'Room'
    no: str = ''

    def info(self):
        """get the simple info"""
        return f'[{self.type}]\t名称：{self.alias}\t\t编号：[{self.id}]'


class Conv2ConvsPlugin(WechatyPlugin):
    """
    """
    def __init__(
        self,
        options: Optional[WechatyPluginOptions] = None,
        trigger_with_at: bool = True,
        with_alias: bool = True
    ) -> None:
        """init params for conversations to conversations configuration

        Args:
            options (Optional[WechatyPluginOptions], optional): default wechaty plugin options. Defaults to None.
            config_file (str, optional): _description_. Defaults to .wechaty/<PluginName>/config.xlsx.
            expire_seconds (int, optional): start to forward. Defaults to 60.
            command_prefix (str, optional): . Defaults to ''.
            trigger_with_at (bool, optional): _description_. Defaults to True.
        """
        super().__init__(options)

        # 3. save the admin status
        self.admin_status: Dict[str, List[Conversation]] = defaultdict(list)
        self.trigger_with_at = trigger_with_at
        self.with_alias = with_alias
        
        self.talker_desc_cache = {}
    
    async def get_talker_desc(self, msg: Message):
        talker = msg.talker()
        room = msg.room()

        union_id = talker.contact_id
        if room:
            union_id += room.room_id
        
        if union_id in self.talker_desc_cache:
            return self.talker_desc_cache[union_id]
        
        await talker.ready()
        talker_name = talker.name
        
        if room:
            alias = await room.alias(talker)
            if alias:
                talker_name = alias

            room_name = None
            if room.room_id in self.setting:
                room_name = self.setting[room.room_id]['alias']

            if not room_name:
                await room.ready()
                room_name = await room.topic()
            
            talker_name = f"{talker_name} @ {room_name}"
    
        self.talker_desc_cache[union_id] = talker_name
        return talker_name

    async def forward_message(self, msg: Message, conversation_id: str):
        """forward the message to the target conversations

        Args:
            msg (Message): the message to forward
            conversation_id (str): the id of conversation
        """
        talker_desc = await self.get_talker_desc(msg)

        # 1. get the type of message
        conversations = self.admin_status.get(conversation_id, [])
        if not conversations:
            return

        file_box = None
        if msg.type() in [MessageType.MESSAGE_TYPE_IMAGE, MessageType.MESSAGE_TYPE_VIDEO, MessageType.MESSAGE_TYPE_ATTACHMENT]:
            file_box = await msg.to_file_box()
            file_path = os.path.join(self.cache_dir, "files", file_box.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            await file_box.to_file(file_path, overwrite=True)
            file_box = FileBox.from_file(file_path)

        for conversation in conversations:
            if conversation.type == 'Room':
                forwarder_target = self.bot.Room.load(conversation.id)
            elif conversation.type == 'Contact':
                forwarder_target = self.bot.Contact.load(conversation.id)
            else:
                continue
            
            # TODO: there are some issues in FileBox saying
            if file_box:
                await forwarder_target.say(file_box)

            # 如果是文本的话，是需要单独来转发
            elif msg.type() == MessageType.MESSAGE_TYPE_TEXT:
                text = msg.text()
                if self.with_alias and conversation.alias:
                    text = talker_desc + '\n===============\n' + text
                await forwarder_target.say(text)

            elif forwarder_target:
                await msg.forward(forwarder_target)

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        talker = msg.talker()
        room: Optional[Room] = msg.room()

        conversation_id: str = room.room_id if room else talker.contact_id

        # 2. 判断是否是自己发送的消息
        if msg.is_self() or conversation_id not in self.setting:
            return
        
        text = msg.text()

        if conversation_id in self.admin_status:
            await self.forward_message(msg, conversation_id=conversation_id)
            self.admin_status.pop(conversation_id)
            message_controller.disable_all_plugins(msg)
            return

        # filter the target conversations
        receivers: List[Conversation] = []
        for key, value in self.setting.items():
            value['id'] = key
            if key == conversation_id:
                continue
            receivers.append(Conversation(
                **value
            ))

        if not receivers:
            return

        self.admin_status[conversation_id] = receivers

        if text:
            # set the words to the message
            msg.payload.text = text
            await self.forward_message(msg, conversation_id=conversation_id)
            self.admin_status.pop(conversation_id)

        message_controller.disable_all_plugins(msg)