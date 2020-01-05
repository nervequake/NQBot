#!/usr/bin/python3

import discord
import sys
import asyncio
import redis
import time
import threading

from utils import *

LEADER = ';'

loop = asyncio.get_event_loop()

def background_worker():
    #loop = asyncio.get_event_loop()
    time.sleep(10)
    print("background worker started")
    p = conn.pubsub()
    p.subscribe('event:command')
    while True:
        print("in loop")
        message = p.get_message()
       
        if message:
            if type(message['data']) is int:
                continue
            c = client.get_channel(662707737217728533)
            asyncio.run_coroutine_threadsafe(
                c.send("You sent: {0}".format(message['data'].decode('utf-8'))), loop)
        time.sleep(1)

class SimpleInterface:
    def __init__(self, client):
        self.dc = client
        self.p = PubSub()
        self.p.sub(PubSub.SMPLCMD)
    
    def run(self):
        while not self.dc.is_closed():
            chan, msg = self.p.get()
            if not msg:
                continue

            if msg['act'] == 'send':
                c = self.dc.get_channel(msg['ctx'])
                asyncio.run_coroutine_threadsafe(
                    c.send(msg['data']), loop)
            
            time.sleep(0.01)

        
class DiscordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user}'.format(client))
        self.inter = SimpleInterface(self)
        self.intert = threading.Thread(target=self.inter.run)
        self.intert.start()

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith(LEADER) and len(message.content) > 1:
            msg = {
                'data': message.content[1:],
                'ctx': message.channel.id,
                'usr': message.author.id
            }

            print("sending command")
            self.p.pub(PubSub.COMMAND, msg)
        else:
            msg = {
                'data': message.content,
                'ctx': message.channel.id,
                'usr': message.author.id
            }
        
            self.p.pub(PubSub.MESSAGE, msg)

if __name__ == "__main__":
    client = DiscordClient()
    client.p = PubSub()
    client.run(get_token())
