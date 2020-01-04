#!/usr/bin/python3
import discord
import sys

from utils import *

LEADER = ';'

async def redis_outbound(client):
    print('outbound waiting')
    await client.wait_until_ready()
    print('outbound ready')
    while not client.is_closed():
        msg = client.q.get(Queue.OUTBOUND)

        print('dequeuing {}'.format(msg['data']))

        channel = client.get_channel(msg['ctx'])
        await channel.send(msg['data'])

class OutboundClient(discord.Client):
    async def on_ready(self):
        print('logged in');
        #if you add this to the loop early it waits forever
        self.loop.create_task(redis_outbound(client))

if __name__ == '__main__':
    client = OutboundClient()
    client.q = Queue()
    client.run(get_token());
