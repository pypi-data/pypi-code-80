import os
from flask_restful import Resource, request
from requests.utils import unquote
from ..web import app_auth
from ...config import Config


class Upload(Resource):
    @app_auth.login_required
    def post(self, path: str):
        path = unquote(path)
        return self.post_chunk_upload(path)

    @staticmethod
    def post_chunk_upload(path: str):
        file = request.files['file']
        file_path = os.path.join(Config.SHARE_DIRECTORY, path, file.filename)
        with open(file_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            chunk = file.stream.read()
            f.write(chunk)
        return {
            "status": True,
            "chunkSize": len(chunk),
            "remoteFileSize": os.path.getsize(file_path),
            "filename": file.filename,
        }

    @staticmethod
    def post_multiupload(path: str):
        uploaded = []
        files = request.files
        for file_item in files.items():
            _, file_storage = file_item
            filename = file_storage.filename
            file_path = os.path.join(Config.SHARE_DIRECTORY, path, filename)
            file_storage.save(file_path)
            uploaded.append(filename)
        return {
            "status": True,
            "filename": uploaded,
        }


class UploadRoot(Upload):
    @app_auth.login_required
    def post(self):
        return super().post("")
