from telethon import TelegramClient, events
import logging
from telewater.settings import API_ID, API_HASH, HELP, WATERMARK, X_OFF, Y_OFF
from telewater.watermark import watermark
from telewater.utils import download_image, get_args
import os


# TODO: allow a better terminal logging
# TODO: (optional) send logs to attached logs channel


def single_bot(client: TelegramClient):
# TODO: take the below functions out of single_bot
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        # TODO: authentication for admins and users via deep linking, or "enter your access code"
        await event.respond('Hi! I am alive.')
        raise events.StopPropagation

    @client.on(events.NewMessage(pattern='/help'))
    async def help(event):
        try:
            await event.respond(HELP)
        finally:
            raise events.StopPropagation

    @client.on(events.NewMessage(pattern='/setimg'))
    async def set_image(event):
        # TODO: accept images directly besides urls
        # TODO: show preview on different sizes
        # TODO: allow image resize / compress/ transparent bkrnd

        try:
            image_url = get_args(event.message.text)
            # TODO: if args are empty, ask follow up question to get user-input
            download_image(image_url, 'image.png')
            await event.respond('Done')
        finally:
            raise events.StopPropagation

    @client.on(events.NewMessage(pattern='/setpos'))
    async def set_pos(event):
        try:
            pos_arg = get_args(event.message.text)
            # TODO: if the pos args are empty, ask follow up question to get user-input of standard postions (TOP/BOTTOM ...)
            #  specific pos must be supplied thru args
            global X_OFF, Y_OFF
            X_OFF, Y_OFF = pos_arg.split('*')
            await event.respond(f'X_OFF = {X_OFF} and Y_OFF = {Y_OFF}')
        finally:
            raise events.StopPropagation

    @client.on(events.NewMessage())
    async def watermarker(event):
        # TODO: reject large files (above certain file limit)
        # TODO: also watermark photos
        if event.gif or event.video:
            mp4_file = await event.download_media('')
            # TODO: suffix the downloaded media with time-stamp and user id
            # TODO: prevent multi user clash
            outf = watermark(mp4_file, X_OFF, Y_OFF)
            print(outf)
            await client.send_file(event.sender_id, outf)
            os.remove(mp4_file)
            os.remove(outf)

    if WATERMARK:
        download_image(url=WATERMARK, filename='image.png')
    # TODO: fetch information about bot name
    # TODO:set the bot commands

        # client(functions.bots.SetBotCommandsRequest(
        #     commands=[types.BotCommand(
        #         command='some string here',
        #         description='some string here'
        #     )]
        # ))
    client.run_until_disconnected()



def run_single_bot(name, tkn):
    os.makedirs(name, exist_ok=True)
    os.chdir(name)
    # TODO: the directory for bot should be /home/watermarker/bot_name
    # the bot can be run via command from anywhere
    client = TelegramClient(name, API_ID, API_HASH).start(bot_token=tkn)
    print(f'Starting bot {name}')
    single_bot(client)
