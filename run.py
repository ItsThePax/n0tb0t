import logging
import TwitchSocket
import GroupChatSocket
import Bot
from config import SOCKET_ARGS

logging.basicConfig(filename='error-log.txt',level=logging.DEBUG)
TS = TwitchSocket.TwitchSocket(**SOCKET_ARGS)
GCS = GroupChatSocket.GroupChatSocket(**SOCKET_ARGS)
bot = Bot.Bot(TS, GCS)

messages = ""

while True:
    read_buffer = TS.s.recv(1024) # GCS.s.recv(1024) to get whispers and stuff

    messages = messages + read_buffer.decode('utf-8')
    last_message = messages.split('\r\n')[-2]
    print(last_message.encode('utf-8'))
    messages = ""
    if last_message == 'PING :tmi.twitch.tv':
        resp = last_message.replace("PING", "PONG") + "\r\n"
        TS.s.send(resp.encode('utf-8'))
    else:
        try:
            bot._act_on(last_message)
        except Exception as e:
            logging.exception("Something went wrong")
            TS.send_message("Something went wrong. The error has been logged.")