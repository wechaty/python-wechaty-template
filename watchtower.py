"""watch tower for keep the alive of running container"""
from __future__ import annotations
import asyncio
from typing import List, Optional
import requests
import docker
from docker.models.containers import Container
from wechaty_puppet import get_logger


logger = get_logger("WatchTower", file='watch-tower.log')


class WatchTower:
    """watchtower to keep container alive"""
    def __init__(self, name_or_id: str, interval_seconds: int = 60, port: int = 8003, try_times: int = 10) -> None:
        """init function

        Args:
            name_or_id (str): name or id of bot container
            interval_seconds (int, optional): . Defaults to 60.
            port (int, optional): the target port of bot service. Defaults to 8003.
            try_times (int, optional): try to check the alive status of bot container
        """
        self.name_or_id = name_or_id
        self.interval_seconds = interval_seconds
        self.port = port
        self.try_times = try_times
        
    def find_bot_container(self) -> Optional[Container]:
        """find the bot container"""
        client = docker.from_env()
        containers: List[Container] = client.containers.list() or []
        for container in containers:
            if container.name == self.name_or_id or container.id == self.name_or_id:
                return container
        return None

    def check_is_alive(self):
        """check if the bot is alive"""
        endpoint = f'http://localhost:{self.port}/ding'
        for _ in range(self.try_times):
            try:
                # 如果在60秒之内没有得到回复，可判断机器人的状态不是很良好
                requests.get(endpoint, timeout=60)

                # 如果返回了结果，可以判断bot正常运行，于是可返回其正常状态
                return True
            except:
                pass
        return False

    async def watch(self):
        """the main body of wathing"""
        logger.info('staring to watch the bot in docker ...')
        while True:
            container = self.find_bot_container()

            if container is not None:
                if not self.check_is_alive():
                    logger.error('===============================================================')
                    logger.error('the bot is not alive. we are trying to restart the container ...')
                    logger.error('===============================================================')
                    container.restart()
                else:
                    logger.info('the bot is alive ...')
            else:
                logger.error('can not find the container of the bot')
            await asyncio.sleep(self.interval_seconds)


if __name__ == '__main__':
    watch_tower = WatchTower(name_or_id='id-of-bot-container', interval_seconds=180)
    asyncio.run(watch_tower.watch())
