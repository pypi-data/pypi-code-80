from .assets import assets


from io import IOBase as FileType
from io import BytesIO


class Uploader:
    __slots__ = ('__api', '__http', '__assets')

    def __init__(self, api):
        self.__api = api
        self.__http = api.http
        self.__assets = assets


    async def photo_messages(self, photos):
        response = await self.__api.photos.getMessagesUploadServer(peer_id = 0)
        response = await self.__http.post(response.upload_url, data = self.convertAsset(photos))
        response = await response.json(content_type = None)

        return await self.__api.photos.saveMessagesPhoto(**response)

        
    async def photo_group_widget(self, photo, image_type):
        response = await self.__api.appWidgets.getGroupImageUploadServer(image_type = image_type)
        response = await self.__http.post(response.upload_url, data = self.convertAsset(photo))
        response = await response.json(content_type = None)

        return await self.__api.appWidgets.saveGroupImage(**response)


    async def photo_chat(self, photo, peer_id):
        if peer_id < 2000000000: 
            raise ValueError("Incorrect peer_id")

        else: 
            values = dict()
            values['chat_id'] = peer_id - 2000000000

        response = await self.__api.photos.getChatUploadServer(**values)
        response = await self.__http.post(response.upload_url, data = self.convertAsset(photo))
        response = await response.json(content_type = None)

        return await self.__api.messages.setChatPhoto(file = response['response'])


    async def document(self, document, title=None, tags=None, peer_id=None, doc_type = 'doc', to_wall = None):
        values = {
            'peer_id': peer_id,
            'type': doc_type
        }
        
        response = await self.__api.docs.getMessagesUploadServer(**values) # vk.com/dev/docs.getMessagesUploadServer
        response = await self.__http.post(response.upload_url, data = self.convertAsset(document, sign = 'file'))
        response = await response.json(content_type = None)
        if title: response['title'] = title 
        if tags: response['tags'] = tags

        return await self.__api.docs.save(**response) 


    async def audio_message(self, audio, peer_id=None):
        return await self.document(
            audio,
            doc_type = 'audio_message',
            peer_id = peer_id
            )


    async def story(self, file, file_type,
              reply_to_story=None, link_text=None,
              link_url=None):
        # переписал функцию для историй, так как адаптированная версия с VK_api под aiohttp 
        # выдавала тупо сам результат запроса. Сделал как фреймворку нужно :3

        if file_type == 'photo':
            method = self.__api.stories.getPhotoUploadServer

        elif file_type == 'video':
            method = self.__api.stories.getVideoUploadServer

        else:
            raise ValueError('type should be either photo or video')

        if (not link_text) != (not link_url):
            raise ValueError(
                'Either both link_text and link_url or neither one are required'
            )

        if link_url and not link_url.startswith('__https://vk.com'):
            raise ValueError(
                'Only internal __https://vk.com links are allowed for link_url'
            )

        if link_url and len(link_url) > 2048:
            raise ValueError('link_url is too long. Max length - 2048')

        values = dict()

        values['add_to_news'] = True
        if reply_to_story: values['reply_to_story'] = reply_to_story
        if link_text: values['link_text'] = link_text
        if link_url: values['link_url'] = link_url

        response = await method(**values)
        response = await self.__http.post(response.upload_url, data = self.convertAsset(file, 'file' if file_type == "photo" else 'video_file'))
        response = await response.json(content_type = None)

        return await self.__api.stories.save(upload_results = response.response.upload_result)


    def convertAsset(self, files, sign = 'file'):
        if isinstance(files, (str, bytes)) or issubclass(type(files), FileType):
            response = None

            if isinstance(files, str): 
                response = self.__assets(files, 'rb', buffering = 0)
            elif isinstance(files, bytes): 
                response = self.__assets(files)
            else:
                response = files

            return {
                sign: response
            }

        elif isinstance(files, list):
            files_dict = {}

            for i in range(min(len(files), 5)): # ограничение в пять файлов
                if isinstance(files[i], (str, bytes)) or issubclass(type(files[i]), FileType):
                    response = None

                    if isinstance(files[i], str): 
                        response = self.__assets(files[i], 'rb', buffering = 0)
                    elif isinstance(files[i], bytes): 
                        response = BytesIO(files[i])
                    else:
                        response = files[i]

                    files_dict[sign + str(i+1)] = response

                else:
                    raise TypeError("Only str, bytes or file-like objects")

            return files_dict

        else:
            raise TypeError("Only str, bytes or file-like objects")