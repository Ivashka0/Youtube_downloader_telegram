import telebot
from random import randint
import os
import json
from pytube import YouTube
from telebot import types

config = {
    "name": "YouTube Downloader",
    "token": "5867025899:AAGbDFmAatXdMkcgV-Y1weUlpQAwSNJTK2Q"
}

fedo = telebot.TeleBot(config["token"])


@fedo.callback_query_handler(func=lambda call: True)
def callback_data(call):
    data = call.data.split('|')
    download_video(data[0], data[1])
    stats = os.stat(f"1.mp4").st_size
    if call.data:
        if stats < 52428800:
            print(str(data))
            print(call.message.chat.id)
            print(call.message.id)
            fedo.delete_message(call.message.chat.id, message_id=call.message.message_id)
            fedo.send_video(chat_id=call.message.chat.id, video=open('1.mp4', 'rb'), supports_streaming=True)
        else:
            fedo.delete_message(call.message.chat.id, message_id=call.message.message_id)
            fedo.send_message(call.message.chat.id, f"Size of file is {round(stats / 1048576, 1)} mb.Unfortunately, "
                                                    f"i can't send more than 50 mb in Telegram, "
                                                    f"so put lower quality lower")


@fedo.message_handler(content_types=["text"])
# ^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$
def get_text(message):
    if message.text.lower() == "download":
        url = fedo.send_message(message.chat.id, f"Write your youtube url:")
        fedo.register_next_step_handler(url, get_quality)
    elif message.text.lower() == "help":
        fedo.send_message(message.chat.id, f"Write `download` and after that type the url of Youtube video")
    else:
        fedo.send_message(message.chat.id, f"If you need help,write 'help' and you will receive a help list ")


def get_quality(message):
    yt = YouTube(message.text)

    my_streams = yt.streams.filter(file_extension='mp4', progressive=True)
    inlines = telebot.types.InlineKeyboardMarkup()
    for streams in my_streams:
        print(f"Video itag : {streams.itag} Resolution : {streams.resolution} VCodec : {streams.codecs[0]}")
        inlines.add(telebot.types.InlineKeyboardButton(text=f"{streams.resolution}",
                                                       callback_data=f"{streams.itag}|{message.text}|"))
    fedo.send_message(message.chat.id, f"Choose quality:", reply_markup=inlines)


def download_video(number, mes):
    yt = YouTube(mes)
    video = yt.streams.get_by_itag(number)

    video.download(filename=f"1.mp4")


fedo.polling(none_stop=True, interval=0)