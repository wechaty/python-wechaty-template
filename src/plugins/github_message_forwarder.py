"""Plugins for Github Message forwarder"""
from __future__ import annotations
from dataclasses import dataclass
import os

from typing import Dict, List, Optional, Union
import requests

from wechaty import Contact, UrlLink, WechatyPlugin, WechatyPluginOptions, Wechaty, Message
from wechaty_puppet import UrlLinkPayload
from wechaty_plugin_contrib.message_controller import message_controller
from github import Github

from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from github.Issue import Issue
from github.IssueComment import IssueComment


GITHUB_URL_LINK_TYPES = ['issue', 'issue-comment', 'pull-request', 'pull-request-comment', 'pull-request']

@dataclass
class GithubUrlLinkPayload(UrlLinkPayload):
    full_name: Optional[str] = None
    type: str = "issue"


class GithubAppMessageParser:
    def __init__(self, token: str) -> None:
        self.github: Github = Github(login_or_token=token)

    def parse(self, message: dict) -> Optional[Union[Issue,
                                               IssueComment,
                                                     PullRequest, PullRequestComment
                                                     ]]:
        event, payload = message['event'], message['payload']
        trigger_name = f"{event}.{payload['action']}"

        if trigger_name == "pull_request.opened":
            return self.parse_pull_request_opened(payload)

        if trigger_name == 'issues.opened':
            return self.parse_issue_opened(payload)

        if trigger_name == 'issue_comment.created':
            return self.parse_issue_comment(payload)

    
    def parse_issue_comment(self, message: dict) -> UrlLinkPayload:
        full_name = message['repository']['full_name']
        issue_number = message['issue']['number']
        description = message['comment']['body']
        avatar_url = message['comment']['user']['avatar_url']
        title=f"Issue#{issue_number} {message['issue']['title'][:30]} {full_name}"
        if "pull_request" in message['issue']:
            title=f"PR#{issue_number} {message['issue']['title'][:30]} {full_name}"

        return GithubUrlLinkPayload(
            url=message['comment']['html_url'],
            title=title[:30],
            description=description[:70],
            thumbnailUrl=avatar_url,
        )
    
    def parse_issue_opened(self, message: dict) -> UrlLinkPayload:
        """parse open issue message to UrlLinkPayload

        Args:
            message (dict): _description_

        Returns:
            UrlLinkPayload: _description_
        """
        full_name = message['repository']['full_name']
        issue_number = message['issue']['number']
        description = message['issue']['body']
        avatar_url = message['issue']['user']['avatar_url']
        title=f"New Issue#{issue_number} {message['issue']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['issue']['html_url'],
            title=title[:30],
            description=description[:70],
            thumbnailUrl=avatar_url,
        )
    
    def parse_pull_request_opened(self, message: dict) -> UrlLinkPayload:
        """parse open issue message to UrlLinkPayload

        Args:
            message (dict): _description_

        Returns:
            UrlLinkPayload: _description_
        """
        full_name = message['repository']['full_name']
        pull_request_number = message['pull_request']['number']
        pull_request_body = message['pull_request']['body']
        avatar_url = message['pull_request']['user']['avatar_url']
        title=f"New PR#{pull_request_number} {message['pull_request']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['pull_request']['html_url'],
            title=title[:30],
            description=pull_request_body[:70],
            thumbnailUrl=avatar_url,
        )

    def parse_pull_request_review_submit_opened(self, message: dict) -> UrlLinkPayload:
        """parse open issue message to UrlLinkPayload

        Args:
            message (dict): _description_

        Returns:
            UrlLinkPayload: _description_
        """
        full_name = message['repository']['full_name']
        pull_request_number = message['pull_request']['number']
        pull_request_body = message['review']['body'] or ''
        avatar_url = message['review']['user']['avatar_url']
        title=f"#{pull_request_number} {message['pull_request']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['pull_request']['html_url'],
            title=title[:30],
            description=pull_request_body[:70],
            thumbnailUrl=avatar_url,
        )

    def parse_pull_request_review_comment_opened(self, message: dict) -> UrlLinkPayload:
        """parse open issue message to UrlLinkPayload

        Args:
            message (dict): _description_

        Returns:
            UrlLinkPayload: _description_
        """
        full_name = message['repository']['full_name']
        pull_request_number = message['pull_request']['number']
        pull_request_body = message['comment']['body'] or ''
        avatar_url = message['comment']['user']['avatar_url']
        title=f"#{pull_request_number} {message['pull_request']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['comment']['html_url'],
            title=title[:30],
            description=pull_request_body[:70],
            thumbnailUrl=avatar_url,
        )


class GithubMessageForwarderPlugin(WechatyPlugin):
    def __init__(self, endpoint: Optional[str] = None, token: Optional[str] = None):
        super().__init__()
        self.endpoint = endpoint

        token = token or os.environ.get("github_token", None)
        self.url_link_parser = GithubAppMessageParser(token)

    async def fetch_url_link(self):
        response = requests.get(self.endpoint)
        messages = response.json().get('data', [])

        self.logger.info(f"start to fetch github url_link status<{response.status_code}> messages<{len(messages)}> ...")

        for message in messages:
            url_link = self.url_link_parser.parse(message)
            if not url_link:
                continue

            for contact_id in self.setting.get("admins", []):
                contact: Contact = self.bot.Contact.load(contact_id)
                await contact.say(UrlLink(url_link))

            return

    async def init_plugin(self, wechaty: Wechaty) -> None:
        # await self.fetch_url_link()
        self.add_interval_job(minutes=1, handler=self.fetch_url_link, job_id=self.name)

    # @message_controller.may_disable_message
    # async def on_message(self, msg: Message) -> None:
    #     if msg.text() == "testing":
    #         await self.fetch_url_link()
    #         message_controller.disable_all_plugins(msg)
    