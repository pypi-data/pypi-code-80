import os
from os import path
from ..utils import Container, BotifyLogger
from traceback import format_exc
from time import sleep

class BotifyMedia():

    PHOTO_EXT = ["jpg", "jpeg", "png"]
    AUDIO_EXT = ["mp3", "wav"]
    ANIMATION_EXT = ["gif"]
    VIDEO_EXT = ["mp4"]
    VOICE_EXT = ["ogg"]

    def __init__(self, botify):
        self.botify = botify
        self.logger = BotifyLogger("media", botify.logger)
        config = botify.config.media
        
        self.channel = config.channel
        self.root = config.get("root", "media")
        self.photo = config.get("photo", self.root)
        self.document = config.get("document", self.root)
        self.animation = config.get("animation", self.root)
        self.audio = config.get("audio", self.root)
        self.voice = config.get("voice", self.root)
        self.video = config.get("video", self.root)
        self.video_note = config.get("video-note", self.root)

        self.create_or_get_all()

    def create_or_get_all(self):
        cwd = os.getcwd()
        
        root_path = path.join(cwd, self.root)
        photo_path = path.join(cwd, self.photo)
        document_path = path.join(cwd, self.document)
        animation_path = path.join(cwd, self.animation)
        audio_path = path.join(cwd, self.audio)
        voice_path = path.join(cwd, self.voice)
        video_path = path.join(cwd, self.video)
        video_note_path = path.join(cwd, self.video_note)

        if not path.exists(root_path): os.mkdir(root_path)
        if not path.exists(photo_path): os.mkdir(photo_path)
        if not path.exists(document_path): os.mkdir(document_path)
        if not path.exists(animation_path): os.mkdir(animation_path)
        if not path.exists(audio_path): os.mkdir(audio_path)
        if not path.exists(voice_path): os.mkdir(voice_path)
        if not path.exists(video_path): os.mkdir(video_path)
        if not path.exists(video_note_path): os.mkdir(video_note_path)

        return [
            root_path, photo_path, document_path, audio_path, 
            voice_path, video_path, video_note_path, animation_path
        ]

    def list_all(self):
        result = []
        _paths_checked = []
        for _path in self.create_or_get_all():
            if not _path in _paths_checked:
                _paths_checked.append(_path)
                for entity in os.listdir(_path):
                    full_entity_path = path.join(_path, entity)
                    if path.isfile(full_entity_path): 
                        if not full_entity_path in result:
                            result.append(full_entity_path)
        return result

    async def update_media(self, *args):
        logger = self.logger
        botify = self.botify
        bot = botify.bot
        botify.me = await bot.get_me()
        logger.info("Updating bot's media library.")
        try:
            for _path in self.list_all():
                file_ = path.split(_path)[1]
                splitted = file_.rsplit(".", maxsplit = 1)
                filename = splitted[0]
                extension = splitted[1].lower()

                media = self.get(filename, warn_on_not_found = False)
                media_valid = False
                if media:
                    try:
                        await bot.get_file(media.file_id)
                        logger.info(f"- File [{file_}] - [+] Already exists on a server.")
                        media_valid = True
                    except Exception as e: 
                        if not "Wrong file_id" in str(e): 
                            logger.error(f"Failed to check file: {format_exc()}") 

                if not media_valid:
                    _type = "document"
                    if extension in self.PHOTO_EXT: _type = "photo"
                    if extension in self.ANIMATION_EXT: _type = "animation"
                    if extension in self.AUDIO_EXT: _type = "audio"
                    if extension in self.VIDEO_EXT: _type = "video"
                    if extension in self.VOICE_EXT: _type = "voice"

                    if _type is "photo": 
                        message = await bot.send_photo(self.channel, photo = open(_path, "rb"))
                        file_id = message.photo[0].file_id
                    
                    if _type is "audio": 
                        message = await bot.send_audio(self.channel, audio = open(_path, "rb"))
                        file_id = message.audio.file_id
                    
                    if _type is "video": 
                        message = await bot.send_video(self.channel, video = open(_path, "rb"))
                        file_id = message.video.file_id
                    
                    if _type is "voice": 
                        message = await bot.send_voice(self.channel, voice = open(_path, "rb"))
                        file_id = message.voice.file_id
                    
                    if _type in ("document", "animation"): 
                        message = await bot.send_document(self.channel, document = open(_path, "rb"))
                        file_id = message.document.file_id

                    _path = path.relpath(_path, os.getcwd())
                    logger.info(f"- File [{file_}] - [+] Sent to a server just now.")

                    if media: botify.media.update(
                        botify.media.tag == filename, 
                        type = _type,
                        file_id = file_id,
                        path = _path
                    )
                    
                    else: botify.media.add(
                        tag = filename,
                        type = _type,
                        file_id = file_id,
                        path = _path
                    ) 
                
                sleep(0.2)
        
        except Exception: logger.error(f"Failed to update media: {format_exc()}")

    def get(self, mediatag: str, warn_on_not_found: bool = True) -> Container: 
        if mediatag.startswith("@"): mediatag = mediatag[1:]
        result = self.botify.media.get(self.botify.media.tag == mediatag)
        if not result and warn_on_not_found: self.logger.warning(f"Media [{mediatag}] not found!")
        return result