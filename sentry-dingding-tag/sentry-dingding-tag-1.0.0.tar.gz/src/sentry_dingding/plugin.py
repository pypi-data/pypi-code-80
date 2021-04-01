# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """

    author = "windole"
    version = sentry.VERSION
    description = "Send error counts to DingDing."

    slug = "DingDing"
    title = "DingDing"
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option("access_token", project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option("access_token", group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = "【%s】的项目异常" % event.project.slug

        interfaceContent = ""
        for interface in event.interfaces.values():
            # body = interface.to_email_html(event)
            # if not body:
            #     continue
            text_body = interface.to_string(event)
            interfaceContent = interfaceContent + "### {title} \n\n {text_body}\n\n".format(
                title=interface.get_title(), text_body=text_body
            )

        tagsContent = ""
        for k, v in event.tags:
            tagsContent = tagsContent + "{tag} = **{value}** \n\n".format(tag=k, value=v)

        issueOwner = dict(event.tags).get("issueOwner")
        # 没有指定解决者
        if issueOwner is None:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": "## {title} \n\n > {message} \n\n \n\n ### 标签 \n\n {tagsContent} \n\n [详细信息]({url})".format(
                        title=title,
                        message=event.title or event.message,
                        # interfaceContent=interfaceContent,
                        tagsContent=tagsContent,
                        url="{}events/{}/".format(group.get_absolute_url(), event.event_id),
                    ),
                },
            }
        else:
            tagsContent = tagsContent + "@%s" % issueOwner
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": "## {title} \n\n > {message} \n\n \n\n ### 标签 \n\n {tagsContent} \n\n [详细信息]({url})".format(
                        title=title,
                        message=event.title or event.message,
                        # interfaceContent=interfaceContent,
                        tagsContent=tagsContent,
                        url="{}events/{}/".format(group.get_absolute_url(), event.event_id),
                    ),
                },
                "at": {"atMobiles": ["%s" % issueOwner]},
            }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8"),
        )
