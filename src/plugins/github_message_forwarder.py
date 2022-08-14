"""Plugins for Github Message forwarder"""
from __future__ import annotations
from dataclasses import dataclass
import os

from typing import Dict, List, Optional, Union
import requests

from wechaty import Contact, UrlLink, WechatyPlugin, WechatyPluginOptions, Wechaty
from wechaty_puppet import UrlLinkPayload
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
            return self.parse_issue_opened(payload)
            
        opened_obj = self.parse_opened(message)
        if opened_obj:
            return opened_obj

        comment = self.parse_comment(message)
        return comment
    
    def parse_issue_comment(self, message: dict) -> UrlLinkPayload:
        full_name = message['repository']['full_name']
        issue_number = message['issue']['number']
        description = message['comment']['body']
        avatar_url = message['comment']['user']['avatar_url']
        title=f"#{issue_number} {message['issue']['title'][:30]} {full_name}"
         
        return GithubUrlLinkPayload(
            url=message['comment']['html_url'],
            title=title[:30],
            description=description[:70],
            thumbnailUrl=avatar_url,
            full_name=full_name,
            type='issue.comment'
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
        title=f"#{issue_number} {message['issue']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['issue']['html_url'],
            title=title[:30],
            description=description[:70],
            thumbnailUrl=avatar_url,
            full_name=full_name,
            type='issue.opened'
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
        title=f"#{pull_request_number} {message['pull_request']['title'][:30]} {full_name}"

        return UrlLinkPayload(
            url=message['pull_request']['html_url'],
            title=title[:30],
            description=pull_request_body[:70],
            thumbnailUrl=avatar_url,
            full_name=full_name,
            type='pull_request.opened'
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
            full_name=full_name,
            # TOOD(wj-Mcat): 
            type='pull_request.created'
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
            full_name=full_name,
            type='pull_request.comment'
        )


class GithubMessageForwarderPlugin(WechatyPlugin):
    def __init__(self, endpoint: Optional[str] = None, token: Optional[str] = None):
        super().__init__()
        self.endpoint = endpoint or "http://wj-github.localtunnel.chatie.io/messages/wechaty"

        token = token or os.environ.get("github_token", None)
        self.url_link_parser = GithubAppMessageParser(token)

    async def fetch_url_link(self):
        self.logger.info("start to fetch github url_link ...")
        response = requests.get(self.endpoint)
        for message in response.json().get("data", []):
            url_link = self.url_link_parser.parse(message)
            contact: Contact = self.bot.Contact.load('wxid_gwemn8cbz51621')
            await contact.say(UrlLink(url_link))

    async def init_plugin(self, wechaty: Wechaty) -> None:
        self.add_interval_job(minutes=1, handler=self.fetch_url_link, job_id=self.name)

