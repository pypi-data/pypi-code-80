from rest_framework import status
from rest_framework.response import Response

class Restful_Response(Response):
    @property
    def rendered_content(self):
        renderer = getattr(self, 'accepted_renderer', None)
        accepted_media_type = getattr(self, 'accepted_media_type', None)
        context = getattr(self, 'renderer_context', None)

        assert renderer, ".accepted_renderer not set on Response"
        assert accepted_media_type, ".accepted_media_type not set on Response"
        assert context is not None, ".renderer_context not set on Response"
        context['response'] = self

        media_type = renderer.media_type
        charset = renderer.charset
        content_type = self.content_type

        if content_type is None and charset is not None:
            content_type = "{}; charset={}".format(media_type, charset)
        elif content_type is None:
            content_type = media_type
        self['Content-Type'] = content_type
        if status.is_success(self.status_code):
            ret = renderer.render(self.data, accepted_media_type, context)
        else:
            if type(self.data)==type("string"):
                message=self.data
            elif "message" in self.data:
                message=self.data["message"]
            else:
                message=""
            return_data={"error":context['response'].status_text,"message":message}
            # 更改返回status_code（二五仔提的不符合规范，清理）
            # context['response'].status_code=200
            ret = renderer.render(return_data, accepted_media_type, context)
        if isinstance(ret, str):
            assert charset, (
                'renderer returned unicode, and did not specify '
                'a charset value.'
            )
            return ret.encode(charset)

        if not ret:
            del self['Content-Type']

        return ret