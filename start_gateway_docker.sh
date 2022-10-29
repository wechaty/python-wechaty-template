#!/bin/bash

# 设置环境变量
if test -z "$1"
then
    echo "请输入你申请的 padlocal token 作为参数, 再次运行脚本"&&exit
else
    padlocal_prefix="puppet_padlocal_"
    if [[ $1 == *$padlocal_prefix* ]]
    then
        echo "环境变量设置完成, 启动docker"
    else
        echo -e "参数格式错误! 请输入类似以下格式的token:\n puppet_padlocal_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"&&exit
    fi
fi
export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-padlocal"
export WECHATY_PUPPET_PADLOCAL_TOKEN=$1
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN=`python3 -c "import uuid;print(uuid.uuid4())"`
sed -i s/token=.*/token=$WECHATY_TOKEN/g .env

docker run -ti \
  --name wechaty_puppet_service_token_gateway \
  --rm \
  -e WECHATY_LOG \
  -e WECHATY_PUPPET \
  -e WECHATY_PUPPET_PADLOCAL_TOKEN \
  -e WECHATY_PUPPET_SERVER_PORT \
  -e WECHATY_TOKEN \
  -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
  wechaty/wechaty:0.65