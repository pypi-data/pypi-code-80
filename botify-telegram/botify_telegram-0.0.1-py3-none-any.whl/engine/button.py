from aiogram.types import InlineKeyboardButton
from aiogram.types import KeyboardButton, KeyboardButtonPollType
from ..utils import Container

class BotifyButton():
    """
Botify Abstraction level for 

    aiogram.types.InlineKeyboardButton
    aiogram.types.KeyboardButton

    @param text: string text or tag to render
    @param data: callback data to send
    @param url: link to follow
    @param login_url: login link to connect
    @param inline: flag to switch between Inline and Reply button types
    @param inline_query: inline query to switch
    @param inline_query_current_chat: inline query to switch in current chat
    @param pay: invoice payment button flag
    @param contact: request contact. Only compatible with Reply button type
    @param location: request location. Only compatible with Reply button type
    @param poll: request poll. Only compatible with Reply button type
    @param botify: An Botify instance
"""

    @classmethod
    def from_list(cls, l: [list, tuple], botify):
        """
Creates BotifyButton from a list template

Templating:
        
    l[0] -  string text or tag to render\n
    l[1] -  data holder. You can use it to specify: 
            url: #https://google.com, 
            login_url: #login:https://google.com, 
            callback_data: products=1, 
            inline_query: @search,
            inline_query_current_chat: @current:search, 
            pay: *pay,
            text: *text,
            poll: *poll:type,
            contact: *contact,
            location: *location


    @param l: List template
    @param botify: An Botify instance
        """
        
        if not type(l) in (list, tuple): return

        l = list(l)
        if len(l) < 2: 
            botify.logger.error(f"Cannot create button from the {l} list. It must contain at least 2 items.")
            return
        
        text = l[0]
        data_ = l[1]

        data = url = login_url = None
        inline_query = inline_query_current_chat = None
        pay = contact = location = False
        context = None
        inline = True
        poll = None

        if len(l) > 2: context = l[2]
        if not data_: return
        if data_.startswith("@current:"): inline_query_current_chat = data_.split(":", maxsplit = 1)[1]
        elif data_.startswith("#login:"): login_url = data_.split(":", maxsplit = 1)[1]
        elif data_.startswith("*poll:"): poll = data_.split(":", maxsplit = 1)[1]
        elif data_.startswith("@"): inline_query = data_[1:]
        elif data_.startswith("#"): url = data_[1:]
        elif data_ == "*pay": pay = True
        elif data_ == "*contact": contact = True
        elif data_ == "*location": location = True
        elif data_ == "*text": inline = False
        else: data = data_

        return cls(
            text, data, url, login_url, inline, inline_query, inline_query_current_chat,
            pay, contact, location, poll, context, botify = botify
        )
        
    def __init__(self, text = "button", data = None, url = None, login_url = None, inline = True, 
                inline_query = None, inline_query_current_chat = None, pay = False,
                contact = False, location = False, poll = None, context = None, botify = None):

        self.text = text
        self.data = data
        self.url = url
        self.login_url = login_url
        self.inline = inline
        self.inline_query = inline_query
        self.inline_query_current_chat = inline_query_current_chat
        self.pay = pay
        self.contact = contact
        self.location = location
        self.poll = poll
        self.botify = botify
        self.context = context

    def build(self):
        botify = self.botify
        context = self.context
        if context is None: context = Container()
        text = botify.build_text(self.text, render = True, context = context)
        data = botify.render(self.data, context) if self.data else None
        url = botify.render(self.url, context) if self.url else None
        login_url = botify.render(self.login_url, context) if self.login_url else None
        inline_query = botify.render(self.inline_query, context) if self.inline_query else None
        inline_query_current_chat = botify.render(self.inline_query_current_chat, context) if self.inline_query_current_chat else None

        poll = KeyboardButtonPollType(self.poll) if self.poll else None
        if poll or self.contact or self.location or not self.inline:
            return KeyboardButton(
                text = text,
                request_contact = self.contact,
                request_location = self.location,
                request_poll = poll
            )

        return InlineKeyboardButton(
            text = text, 
            url = url, 
            login_url = login_url, 
            callback_data = data, 
            switch_inline_query = inline_query, 
            switch_inline_query_current_chat = inline_query_current_chat,
            pay = self.pay
        )