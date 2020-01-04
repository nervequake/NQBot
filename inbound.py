#!/usr/bin/python3
import discord
import sys

from utils import *

LEADER = ';'

class InboundClient(discord.Client):
    async def on_ready(self):
        print('logged in');

    async def on_message(self, message):
        if message.author == self.user:
            #lets not loop forever
            return

        if message.content.startswith(LEADER) and len(message.content) > 1:
            msg = {
                'data':message.content[1:],
                'ctx':message.channel.id
            }

            print('queuing {}'.format(msg['data']))

            self.q.add(Queue.INBOUND, msg)

if __name__ == '__main__':
    client = InboundClient()
    client.q = Queue()
    client.run(get_token());
