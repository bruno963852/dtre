import os
from logging import StreamHandler

CHANNEL_ID = int(os.environ['CHANNEL_ID'])


class DiscordLoggingHandler(StreamHandler):
    def __init__(self, bot):
        StreamHandler.__init__(self)
        self.bot = bot
        self.channel = bot.get_channel(CHANNEL_ID)
    
    def emit(self, record):
        msg = self.format(record)

        task = self.bot.loop.create_task(self.channel.send(msg))
