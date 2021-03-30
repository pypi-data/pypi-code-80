from os import getenv
from redis import Redis
from requests import post, get


class WeChatEnterprise:
    __DateBaseName = "WeChat"

    def __init__(self, corp_id: str, corp_secret: str, agent_id: str):
        self.r = Redis(host=getenv('REDIS_HOST'), port=int(getenv('REDIS_PORT', default='6379')))
        self.access_token = self.__get_access_token(corp_id, corp_secret)
        self.agent_id = agent_id

    def __get_access_token(self, corp_id: str, corp_secret: str):
        access_token = self.__get_local_access_token()

        if access_token is None:
            response = self.__get_update_access_token(corp_id, corp_secret)
            if response.get('errcode') != 0:
                raise Exception("error code: %d\nerror message: %s" % (response.get('errcode'), response.get("errmsg")))
            access_token = response.get('access_token')
            self.r.setex(name=self.__DateBaseName + '_access_token', time=response.get('expires_in'),
                         value=access_token)

        else:
            access_token = access_token.decode()

        return access_token

    def __get_local_access_token(self):
        return self.r.get(self.__DateBaseName + '_access_token')

    def __get_update_access_token(self, corp_id: str, corp_secret: str):
        response: dict = get(url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
                             params={"corpid": corp_id, "corpsecret": corp_secret}).json()
        return response

    def upload_media(self, media_type: str):
        pass

    def send_text_message(self, to_user: str, content: str, safe: int = 0, enable_duplicate_check: int = 0,
                          duplicate_check_interval: int = 1800, msg_type: str = "text"):
        data = {
            "touser": to_user,
            "msgtype": "text",
            "agentid": self.agent_id,
            "%s" % msg_type: {
                "content": content
            },
            "safe": safe,
            "enable_duplicate_check": enable_duplicate_check,
            "duplicate_check_interval": duplicate_check_interval
        }
        response = post(
            url=" https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.access_token, json=data)
        return response

    def send_media_message(self):
        pass
