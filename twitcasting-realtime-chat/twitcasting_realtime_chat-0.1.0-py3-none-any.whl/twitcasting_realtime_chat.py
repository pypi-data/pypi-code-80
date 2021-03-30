import twitcasting
import websocket
import json
import os
import cursor
import sys
from datetime import datetime


# definition of ansi escape color-codes
class Colors:
    BLACK       = '\033[30m'
    RED         = '\033[31m'
    GREEN       = '\033[32m'
    DARK_GRAY   = '\033[1;30;40m'
    YELLOW      = '\033[33m'
    BLUE        = '\033[34m'
    PURPLE      = '\033[35m'
    CYAN        = '\033[36m'
    BRIGHT_CYAN = '\033[1;36;40m'
    WHITE       = '\033[37m'
    END         = '\033[0m'
    BOLD        = '\033[1;37;40m'
    UNDERLINE   = '\033[4m'
    INVISIBLE   = '\033[08m'
    REVERCE     = '\033[07m'
    

LOG_PREFIX = f"{Colors.GREEN}[TWCS_REALTIME_CHAT]{Colors.END} "


class TwcsRealtimeChat():
    def __init__(self, auto_reconnect: bool = True):
        self.auto_reconnect = True

        self.__ws = None
        self.__cached_user_id = None
        self.__cached_callback = None

    
    def __clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    
    def __set_terminal_title(self, title: str):
        sys.stdout.write(f"\x1b]2;{title}\x07")

    
    def __log(self, *args):
        print(f"{LOG_PREFIX}{''.join(map(str, args)) if args else ''}")


    def __on_message(self, ws, message):
        try:
            # an empty message often sent by the server
            if message == "[]":
                return
            
            datas = json.loads(message)

            for data in datas:
                # timestamp is in milliseconds
                created_at = int(data["createdAt"]) // 100
                timestamp = datetime.fromtimestamp(created_at).strftime("%M:%S")
                
                author_name = data["author"]["name"]
                chat_message = data["message"].replace("\n", "")
                prefix = f"{Colors.DARK_GRAY}[{timestamp}] {Colors.BRIGHT_CYAN}{author_name}: {Colors.END}"

                print(f"{prefix}{Colors.BOLD}{chat_message}{Colors.END}")
        except Exception as ex:
            self.__log(f"[ERR]: {ex}")


    def __on_error(self, ws, error):
        self.__log(f"failed to connect to the server")


    def __on_close(self, ws):
        self.__log(f"connection closed")

        if self.auto_reconnect:
            self.run(self.__cached_user_id, self.__cached_callback)


    def __on_open(self, ws):
        self.__log(f"connected has been opened")


    def run(
        self,
        user_id: str,
        callback: type(lambda msg: print) = __on_message
    ):
        """
        Run the real-time chat

        Parameters
        ----------
        user_id: str
            The target user's id
        callback: function
            The callback function that called
            when the message is arrived
        """

        try:
            self.__clear_console()
            cursor.hide()
        except:
            pass

        # cache call parameters in order to reconnect
        self.__cached_user_id = user_id
        self.__cached_callback = callback

        self.__log(f"retriving live video id...")
        # video id is necessary to get event pub-sub socket address
        video_id = twitcasting.get_video_id(user_id)
        self.__log(f"got live video id {video_id}")

        # get event pub-sub socket address
        sock_address = twitcasting.get_event_pubsub_url(video_id)

        self.__ws = websocket.WebSocketApp(
            sock_address,
            on_open = self.__on_open,
            on_message = self.__on_message,
            on_error = self.__on_error,
            on_close = self.__on_close,
        )

        try:
            self.__set_terminal_title(f"twcs_realtime_chat ({video_id})")
        except:
            pass

        self.__ws.run_forever()