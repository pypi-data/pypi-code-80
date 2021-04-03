import simplebot
from deltachat import Message
from simplebot.bot import Replies

__version__ = "1.0.0"


@simplebot.filter
def filter_messages(message: Message, replies: Replies) -> None:
    """Process messages with failed encryption."""
    if message.error:
        replies.add(
            text="I was not able to decrypt this message, please repeat.", quote=message
        )


class TestPlugin:
    def test_filter(self, mocker):
        msgs = mocker.get_replies("no error")
        assert not msgs

        msg = mocker.make_incoming_message("with error")
        msg.error = True
        reply = mocker.get_one_reply(msg=msg)
        assert "please repeat" in reply.text
