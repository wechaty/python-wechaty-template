# python-wechaty-template

Python Wechaty Project Template which contains the best practise.

## Getting Started

### 申请Token

如要运行微信机器人，需要申请Token来启动服务，在此推荐申请[Padlocal Token](http://pad-local.com/#/)来快速启动该服务。

### 启动Gateway Docker 服务

```shell
# 设置环境变量

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-padlocal"
export WECHATY_PUPPET_PADLOCAL_TOKEN="{{puppet_padlocal_XXXXXX}}"

# export WECHATY_PUPPET_SERVER_PORT="{{open-service-port}}"
export WECHATY_PUPPET_SERVER_PORT="8080"
# 可使用代码随机生成UUID：import uuid;print(uuid.uuid4());
export WECHATY_TOKEN="{{your-custom-id}}"

docker run -ti \
  --name wechaty_puppet_service_token_gateway \
  --rm \
  -e WECHATY_LOG \
  -e WECHATY_PUPPET \
  -e WECHATY_PUPPET_PADLOCAL_TOKEN \
  -e WECHATY_PUPPET_SERVER_PORT \
  -e WECHATY_TOKEN \
  -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
  wechaty/wechaty:0.56
```

以上脚本当中，只需要调整三个地方：

* WECHATY_PUPPET_PADLOCAL_TOKEN: 申请的Padlocal Token
* WECHATY_PUPPET_SERVER_PORT: 服务器暴露的端口，要确保该端口外部可访问性
* WECHATY_TOKEN: 自定义的WechatyToken，建议使用生成的uuid

### 安装依赖

```shell
pip install -r requirements.txt
```

### 设置环境变量

将以上生成的`your-custom-id`添加到`.env`文件中。

### 运行机器人

```shell
python bot.py
```

初次登陆时，可能需要多次扫码才会登陆成功。

## History


### v0.0.1 (July 2022)

The `python-wechaty-template` project was created. 

## Maintainers

- @wj-Mcat - [wj-Mcat](https://github.com/wj-Mcat), nlp researcher

## Copyright & License

- Code & Docs © 2022 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
