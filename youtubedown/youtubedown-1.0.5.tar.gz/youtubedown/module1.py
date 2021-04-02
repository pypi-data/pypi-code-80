from youtube_dl import YoutubeDL
import youtube_dl
import asyncio



class asyncmodule():
    def __init__(self, title: str):
        self.title = title
        
    async def urldown(self, title: str, nick: str):
        video = False
        loop = asyncio.get_event_loop()
        YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': f'{nick}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }       
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(title, download=True))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        if 'entries' in data:
            try:
                video = data['entries'][0]
            except:
                return {"result": False, "json_result": False}
        list0 = ['channel','channel_url','title','description','video_url','duration','thumbnail','audio_source','view_count']
        list = ['uploader','uploader_url','title','description','webpage_url','duration','thumbnail','formats','view count']
        datas = {}
        if not video: return {'result': True, 'json_result': False}
        for i in range(0, 9):
            try:
                if list[i] == "formats":
                    datas[list0[i]] = video[list[i]][0]['url']
                else:
                    datas[list0[i]] = video[list[i]]
            except:
                pass
        
        datas['result'] = True
        datas['json_result'] = True
        return datas
    async def titledown(self, title: str, nick: str):
        video = False
        loop = asyncio.get_event_loop()
        YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': f'{nick}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }   
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info("ytsearch:{0}".format(title), download=True))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        if 'entries' in data:
            try:
                video = data['entries'][0]
            except:
                return {"result": False, "json_result": False}
        list0 = ['channel','channel_url','title','description','video_url','duration','thumbnail','audio_source','view_count']
        list = ['uploader','uploader_url','title','description','webpage_url','duration','thumbnail','formats','view count']
        datas = {}
        if not video: return {'result': True, 'json_result': False}
        for i in range(0, 9):
            try:
                if list[i] == "formats":
                    datas[list0[i]] = video[list[i]][0]['url']
                else:
                    datas[list0[i]] = video[list[i]]
            except:
                pass
        datas['result'] = True
        datas['json_result'] = True
        return datas
    async def urlsearch(self, title: str):
        video = False
        loop = asyncio.get_event_loop()
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(title, download=False))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        if 'entries' in data:
            try:
                video = data['entries'][0]
            except:
                return {"result": False, "json_result": False}
        list0 = ['channel','channel_url','title','description','video_url','duration','thumbnail','audio_source','view_count']
        list = ['uploader','uploader_url','title','description','webpage_url','duration','thumbnail','formats','view count']
        datas = {}
        if not video: return {'result': True, 'json_result': False}
        for i in range(0, 9):
            try:
                if list[i] == "formats":
                    datas[list0[i]] = video[list[i]][0]['url']
                else:
                    datas[list0[i]] = video[list[i]]
            except:
                pass
        datas['result'] = True
        datas['json_result'] = True
        return datas
    async def titleserach(self, title: str):
        video = False
        loop = asyncio.get_event_loop()
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info("ytsearch:{0}".format(title), download=False))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        if 'entries' in data:
            try:
                video = data['entries'][0]
            except:
                return {"result": False, "json_result": False}
        list0 = ['channel','channel_url','title','description','video_url','duration','thumbnail','audio_source','view_count']
        list = ['uploader','uploader_url','title','description','webpage_url','duration','thumbnail','formats','view count']
        datas = {}
        if not video: return {'result': True, 'json_result': False}
        for i in range(0, 9):
            try:
                if list[i] == "formats":
                    datas[list0[i]] = video[list[i]][0]['url']
                else:
                    datas[list0[i]] = video[list[i]]
            except:
                pass
        datas['result'] = True
        datas['json_result'] = True
        return datas
