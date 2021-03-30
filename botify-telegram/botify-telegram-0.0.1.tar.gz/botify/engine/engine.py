import math
from traceback import format_exc
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.types import InputMediaPhoto, InputMediaAnimation, InputMediaAudio
from aiogram.types import InputFile, InputMediaDocument, InputMediaVideo
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageCantBeEdited, BadRequest
from ..utils import Container, BotifyLogger
from .button import BotifyButton
from jinja2 import Environment

class BotifyEngine():
    def __init__(self, botify):
        self.botify = botify
        self.dispatcher = botify.dispatcher
        self.logger = BotifyLogger("engine", botify.logger)

    def to_message(self, message_dict): return Message.to_object(message_dict)

    async def check_subscriptions(self, user_id):
        botify = self.botify
        need_to_subscribe = []
        if type(botify.context.subscription) is list:
            for data in botify.context.subscription:
                channel = data.link
                if not await self.is_subscribed(user_id, channel):
                    need_to_subscribe.append(data)
        return need_to_subscribe

    async def is_subscribed(self, user_id, group_id):
        try:
            result = await self.botify.bot.get_chat_member(group_id, user_id)
            if result.status == "left": return False
        except BadRequest: return False
        except: self.logger.error(f"Failed to check subscription ({user_id}, {group_id}): {format_exc()}") 
        return True

    async def callback_wrapper(self, callback, require, save_media, entity, state: FSMContext):
        sender = entity.from_user
        botify = self.botify
        logger = self.logger
        try:

            # Insert or update user data

            user = botify.users.get(botify.users.user_id == sender.id)
            data = Container(
                firstname = sender.first_name,
                lastname = sender.last_name if sender.last_name else "",
                username = sender.username if sender.username else ""
            )

            for admin in botify.config.admins:
                if type(admin) is int:
                    if admin == sender.id:
                        data.admin = True
                        data.permissions = 5
                
                if type(admin) is Container:
                    if admin.id == sender.id:
                        data.admin = True
                        data.permissions = admin.permissions

            if not user: user = botify.users.add(
                user_id = sender.id,
                **data
            )
            else: user = botify.users.update(
                botify.users.user_id == sender.id,
                **data
            )[0]

            # Setup context
            
            if type(require) is list:
                for modelname in require:
                    try:
                        query = getattr(botify, modelname)
                        result = query.get_all(query.user_id == sender.id)
                        if type(result) is list:
                            if len(result) == 1: 
                                result = result[0]
                        botify.context[modelname] = result
                    except Exception: logger.error(f"Failed to load user requirement {modelname}: {format_exc()}")

            user.update(await state.get_data({}))
            botify.context.user = user

            if type(entity) is Message: 
                botify.context.message = Container(**entity.to_python())
                
                if save_media:
                    if type(save_media) is bool or (save_media is "*"):
                        save_media = ["photo", "document", "voice", "audio", "video", "video_note"]
                else: save_media = []

                if type(entity.photo) is list:
                    if len(entity.photo) == 1:
                        photo = Container(**entity.photo[0].to_python())
                        if "photo" in save_media: botify.medialib.add_photo(photo)
                        botify.context.photo = photo
                    elif len(entity.photo) > 1: 
                        photos = [Container(**photo.to_python()) for photo in entity.photo]
                        if "photo" in save_media:
                            for photo in photos: 
                                botify.medialib.add_photo(photo)
                        botify.context.photo = photos
                
                if entity.document: 
                    document = Container(**entity.document.to_python())
                    if "document" in save_media: botify.medialib.add_document(document)
                    botify.context.document = document

                if entity.voice: 
                    voice = Container(**entity.voice.to_python())
                    if "voice" in save_media: botify.medialib.add_voice(voice)
                    botify.context.voice = voice

                if entity.video: 
                    video = Container(**entity.video.to_python())
                    if "video" in save_media: botify.medialib.add_video(video)
                    botify.context.video = video

                if entity.video_note: 
                    video_note = Container(**entity.video_note.to_python())
                    if "video_note" in save_media: botify.medialib.add_video_note(video_note)
                    botify.context.video_note = video_note

                if entity.location: botify.context.location = Container(**entity.location.to_python())
                if entity.venue: botify.context.venue = Container(**entity.venue.to_python())
                if entity.poll: botify.context.poll = Container(**entity.poll.to_python())

                if not entity.photo: del botify.context.photo
                if not entity.location: del botify.context.location
                if not entity.document: del botify.context.document
                if not entity.poll: del botify.context.poll
                if not entity.voice: del botify.context.voice
                if not entity.video: del botify.context.video
                if not entity.video_note: del botify.context.video_note
                if not entity.venue: del botify.context.venue

            if type(entity) is CallbackQuery: botify.context.call = Container(**entity.to_python())
            arguments_count = callback.__code__.co_argcount
            args = [entity, user, state, botify.context]
            return await callback(*args[:arguments_count])
        except Exception: logger.error(f"Callback wrapper error: {format_exc()}")

    # Handlers

    def first_start(self, *custom_filters, state = "*", run_task = None, require = None, save_media = None, **kwargs):
        first_check = lambda message: not self.botify.users.get(self.botify.users.user_id == message.from_user.id)
        def decorator(callback):
            async def _callback(message: Message, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, message, state)
            self.dispatcher.register_message_handler(
                _callback, *[*custom_filters, first_check], commands = ["start"],
                state = state, run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def start(self, *custom_filters, state = "*", run_task = None, require = None, save_media = None, **kwargs):
        def decorator(callback):
            async def _callback(message: Message, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, message, state)
            self.dispatcher.register_message_handler(
                _callback, *custom_filters, commands = ["start"],
                state = state, run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def admin(self, *custom_filters, state = "*", run_task = None, require = None, save_media = None, **kwargs):
        admin_check = lambda message: self.botify.users.get(
            self.botify.users.user_id == message.from_user.id
        ).admin
        def decorator(callback):
            async def _callback(message: Message, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, message, state)
            self.dispatcher.register_message_handler(
                _callback, *[*custom_filters, admin_check], commands = ["admin"],
                state = state, run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def admin_message(self, *custom_filters, state = "*", commands = None, regexp = None, content_types = ["text"],
                        run_task = None, require = None, save_media = None, **kwargs
                    ):
        admin_check = lambda message: self.botify.users.get(
            self.botify.users.user_id == message.from_user.id
        ).admin
        def decorator(callback):
            async def _callback(message: Message, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, message, state)
            self.dispatcher.register_message_handler(
                _callback, *[*custom_filters, admin_check], commands = commands,
                regexp = regexp, content_types = content_types, 
                state = state, run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def message(self, *custom_filters, commands = None, regexp = None, content_types = ["text"], 
                state = "*", run_task = None, require = None, save_media = None, **kwargs
            ):
        def decorator(callback):
            async def _callback(message: Message, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, message, state)
            self.dispatcher.register_message_handler(
                _callback, *custom_filters, commands = commands,
                regexp = regexp, content_types = content_types,
                state = state, run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def admin_button(self, *custom_filters, state = "*", run_task = None, require = None, save_media = None, **kwargs):
        admin_check = lambda call: self.botify.users.get(
            self.botify.users.user_id == call.from_user.id
        ).admin
        call_admin_check  = lambda call: call.data.startswith("adm")
        def decorator(callback):
            async def _callback(call: CallbackQuery, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, call, state)
            self.dispatcher.register_callback_query_handler(
                _callback, *[*custom_filters, admin_check, call_admin_check], state = state, 
                run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    def button(self, *custom_filters, state = "*", run_task = None, require = None, save_media = None, **kwargs):
        def decorator(callback):
            async def _callback(call: CallbackQuery, state: FSMContext): 
                return await self.callback_wrapper(callback, require, save_media, call, state)
            self.dispatcher.register_callback_query_handler(
                _callback, *custom_filters, state = state, 
                run_task = run_task, **kwargs
            )
            return _callback
        return decorator

    # Engine

    def render(self, text, context = None):
        env = Environment()
        text = env.from_string(text)
        if context is None: context = Container()
        return text.render(**{**self.botify.context, **context})

    def build_text(self, text, render, context = None):
        if context is None: context = Container()
        text = self.botify.strings.get(text, text)
        if render: text = self.render(text, context)
        return text

    def build_cols(self, buttons, cols = 2):
        _buttons = []
        row = []
        for button in buttons:
            row.append(button)
            if len(row) == cols:
                _buttons.append(row)
                row = []
        _buttons.append(row)
        return _buttons

    def build_pagination(self, page, maxpage, page_data, pagination_data = "none", wrap = False):
        buttons = []
        if page > maxpage: page = maxpage
        if page < 1 and wrap: buttons.append(("btn-prev-page", page_data, {"page": maxpage}))
        if page > 1: buttons.append(("btn-prev-page", page_data, {"page": page - 1}))
        buttons.append(("btn-pagination", pagination_data, {"page": page, "maxpage": maxpage}))
        if page < maxpage: buttons.append(("btn-next-page", page_data, {"page": page + 1}))
        if page == maxpage and page != 1 and wrap: buttons.append(("btn-next-page", page_data, {"page": 1}))
        return buttons if len(buttons) > 1 else []

    def prepare_buttons(self, buttons):
        botify = self.botify
        _buttons = []
        for button in buttons:
            
            if type(button) in (dict, Container):
                if "model" in button.keys():

                    model = getattr(botify, button["model"])
                    page = int(button.get("page", 1))
                    limit = int(button.get("limit", 5))
                    data, count = model.get_all(
                        *button.get("filters", []), 
                        page = page,
                        limit = limit,
                        filter_by = button.get("filter_by", {}),
                        order_by = button.get("order_by", []),
                        count = True
                    )

                    while not data and page > 1:
                        page -= 1
                        data = model.get_all(
                            *button.get("filters", []), 
                            page = page,
                            limit = limit,
                            filter_by = button.get("filter_by", {}),
                            order_by = button.get("order_by", [])
                        )
                        
                    data = [(button.get("button", "btn-item"), button.get("data", "i={{id}}"), {"item": row}) for row in data]
                    cols = button.get("cols", 1)
                    if cols > 1: data = self.build_cols(data, cols)
                    maxpage = math.ceil(count / limit)
                    pagination = self.build_pagination(
                        page, maxpage, 
                        button.get("page-data", "page={{page}}"), 
                        button.get("pagination-data", "none"),
                        button.get("wrap", False)
                    )
                    _buttons.extend(data)
                    _buttons.append(pagination)
            
            else: _buttons.append(button)
        return _buttons

    def build_buttons(self, buttons, context = None):

        if context is None: context = Container()
        if type(buttons) in (InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove): return buttons
        if buttons is "!remove": return ReplyKeyboardRemove()
        if buttons is "!remove:selective": return ReplyKeyboardRemove(True)
        
        reply_markup = ReplyKeyboardMarkup(resize_keyboard = True)
        inline_markup = InlineKeyboardMarkup()

        if type(buttons) in (list, tuple):
            buttons = self.prepare_buttons(buttons)
            for button in buttons:
                if len(button):

                    if type(button[0]) in (list, tuple): 
                        row = []
                        inline = True
                        for button in button:
                            button = BotifyButton.from_list(button, self.botify)
                            if type(button) is BotifyButton: button = button.build()
                            
                            if type(button) is InlineKeyboardButton: 
                                row.append(button)
                                inline = True

                            elif type(button) is KeyboardButton: 
                                row.append(button)
                                inline = False

                        if inline: inline_markup.row(*row)
                        else: reply_markup.row(*row)

                    else:
                        button = BotifyButton.from_list(button, self.botify)
                        if type(button) is BotifyButton: button = button.build()
                        if type(button) is InlineKeyboardButton: inline_markup.row(button)
                        elif type(button) is KeyboardButton: reply_markup.row(button)

        if reply_markup.keyboard: return reply_markup
        if inline_markup.inline_keyboard: return inline_markup

    async def delete(self, message):
        try: await self.botify.bot.delete_message(message.chat.id, message.message_id)
        except Exception: self.logger.warning(f"Failed to delete message: {format_exc()}")

    async def notify(self, call, text, context = None, render = True, alert = False):
        if context is None: context = Container()
        self.botify.context.update(context)
        text = self.build_text(text, render)

        try: return await call.answer(text, show_alert = alert)
        except Exception: self.logger.warning(f"Failed to answer callback query: {format_exc()}")

    async def modal(self, call, text, context = None, render = True): 
        return await self.notify(call, text, context, render, True)

    def prepare_entities(self, text, buttons = None, context = None, render = True):
        botify = self.botify
        if context is None: context = Container()
        botify.context.update(context)

        text = self.build_text(text, render)
        buttons = self.build_buttons(buttons)
        return text, buttons

    async def __send_plain_message(self, id, text, buttons = None, context = None, render = True, preview = False):

        bot = self.botify.bot
        text, buttons = self.prepare_entities(text, buttons, context, render)
        try: return await bot.send_message(id, text, "html", reply_markup = buttons, disable_web_page_preview = not preview)
        except: pass

    async def __send_location(self, id, longitude, latitude, text, buttons = None, context = None, render = True, preview = False):

        bot = self.botify.bot
        text, buttons = self.prepare_entities(text, buttons, context, render)
        try: return await bot.send_location(id, latitude, longitude, reply_markup = buttons)
        except Exception: return await self.__send_plain_message(id, text, buttons, context, render = False, preview = preview)

    async def __send_type(self, id, media, text, buttons = None, context = None, render = True, _type = "photo", preview = False):

        bot = self.botify.bot
        if _type == "animation": _type = "document"
        text, buttons = self.prepare_entities(text, buttons, context, render)
        try: return await getattr(bot, f"send_{_type}")(id, media, text, "html", reply_markup = buttons)
        except Exception: return await self.__send_plain_message(id, text, buttons, context, render = False, preview = preview)

    async def __edit_plain_message(self, message: Message, text, buttons = None, context = None, render = True, preview = False):

        text, buttons = self.prepare_entities(text, buttons, context, render)
        try: return await message.edit_text(text, "html", reply_markup = buttons, disable_web_page_preview = not preview)
        except Exception: 
            await self.delete(message)
            return await self.__send_plain_message(message.chat.id, text, buttons, context, render, preview)

    async def __edit_location(self, message, longitude, latitude, text, buttons = None, context = None, render = True, preview = False):

        text, buttons = self.prepare_entities(text, buttons, context, render)
        await self.delete(message)
        return await self.__send_location(message.chat.id, longitude, latitude, text, buttons, context, render = False, preview = preview)

    async def __edit_type(self, message: Message, media, text, buttons = None, context = None, render = True, _type = "photo", preview = False):
        text, buttons = self.prepare_entities(text, buttons, context, render)
        if _type == "photo": _media = InputMediaPhoto(media, text, "html")
        if _type == "document": _media = InputMediaDocument(media, text, "html")
        if _type == "animation": _media = InputMediaAnimation(media, text, "html")
        if _type in ("audio", "voice"): _media = InputMediaAudio(media, text, "html")
        if _type in ("video", "video_note"): _media = InputMediaVideo(media, text, "html")
        try: return await message.edit_media(_media, buttons)
        except Exception: 
            await self.delete(message)
            return await self.__send_type(message.chat.id, media, text, buttons, context, render, _type, preview)

    async def send(self, id, text, media = None, location = None, buttons = None, context = None, render = True, preview = False):
        
        botify = self.botify
        if type(media) is str:
            if media.startswith("@"):
                media = botify.medialib.get(media)

        if location: 
            
            if type(location) in (list, tuple):
                longitude = location[0]
                latitude = location[1]
            
            if type(location) in (dict, Container):
                longitude = location["longitude"]
                latitude = location["latitude"]

            return await self.__send_location(id, longitude, latitude, text, buttons, context, render, preview)
        if media: return await self.__send_type(id, media.file_id, text, buttons, context, render, media.type, preview)
        return await self.__send_plain_message(id, text, buttons, context, render, preview)

    async def edit(self, message, text, media = None, location = None, buttons = None, context = None, render = True, preview = False):
        
        botify = self.botify
        if type(media) is str:
            if media.startswith("@"):
                media = botify.medialib.get(media)

        if location: 
            
            if type(location) in (list, tuple):
                longitude = location[0]
                latitude = location[1]
            
            if type(location) in (dict, Container):
                longitude = location["longitude"]
                latitude = location["latitude"]

            return await self.__edit_location(message, longitude, latitude, text, buttons, context, render, preview)
        if media: return await self.__edit_type(message, media.file_id, text, buttons, context, render, media.type, preview)
        return await self.__edit_plain_message(message, text, buttons, context, render, preview)