# python-wechaty-template

Python Wechaty Project Template which contains the best practise.

## Getting Started

### 申请Token

如要运行微信机器人，需要申请Token来启动服务，在此推荐申请[Padlocal Token](http://pad-local.com/#/)来快速启动该服务。

### 启动Gateway Docker 服务
运行本项目下的`start_gateway_docker.sh`脚本，并将申请到的Padlocal Token作为脚本参数传入

```shell
./start_gateway_docker.sh <your_token>
```

### 运行机器人

```shell
make bot
```

初次登陆时，可能需要多次扫码才会登陆成功。
扫码登陆成功后，wechaty机器人就算启动成功了，可以通过微信向机器人发送消息`ding`来测试。默认开启DingDong插件，机器人会自动回复`dong`。
至此，恭喜你，你的第一个微信机器人成功运行了！接下来可以将各种需求和业务逻辑以插件的形式加入到机器人中。

## 编写插件

目前有很多开发者将所有的业务逻辑都写在一个文件的一个函数（`on_message`）里面，时间长了，业务多了，就导致这里的代码很难管理，故需要从代码文件层面就将业务隔离开，此时我们推荐使用[插件系统](https://wechaty.readthedocs.io/zh_CN/latest/plugins/introduction/)来编写对应业务。

* 插件示例

```python
from wechaty import WechatyPlugin, Message

class DingDongPlugin(WechatyPlugin):
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say("dong")
```

* 插件消息传递

如果在Bot中use了很多个插件：[A, B, C, D, E, ...]，wechaty接收到消息之后会挨个儿将消息传递给插件去处理，如果其中回复了消息之后，想阻止插件继续传递的话，需要添加一个message_controller模块，代码示例如下：

```python
from wechaty import WechatyPlugin, Message
from wechaty_plugin_contrib.message_controller import message_controller

class DingDongPlugin(WechatyPlugin):

    @message_controller
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say("dong")
            message_controller.disable_all_plugins(msg)
```

对代码的修改只需要三行修改：
* 添加message_controller全局单例对象的导入
* 将其作为装饰器应用在on_message函数上
* 在想阻止消息传递的地方添加一行代码：`message_controller.disable_all_plugins(msg)`，此时需要注意需要将msg对象传递进去。

## History

### v0.0.2 (Aug 2022)

add `wechaty-ui` based code.

### v0.0.1 (July 2022)

The `python-wechaty-template` project was created. 

## Maintainers

- @wj-Mcat - [wj-Mcat](https://github.com/wj-Mcat), nlp researcher

## Copyright & License

- Code & Docs © 2022 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
