#!/usr/bin/python3
import discord
import redis
import sys
import json

LEADER = ';'
INBOUND = 'inbound'
OUTBOUND = 'outbound'

token = ''
with open('token', 'r') as tk:
    token = tk.read().strip()

r = redis.Redis(host='localhost', port=6379, db=0)

class ReadClient(discord.Client):
    async def on_ready(self):
        print('logged in');

    async def on_message(self, message):
        if message.content.startswith(LEADER):
            msg = {
                'data':message.content,
                'src':message.channel.id
            }

            print('queuing {}'.format(msg['data']))

            r.lpush(INBOUND, json.dumps(msg))

class WriteClient(discord.Client):
    async def on_ready(self):
        print('logged in');

async def redis_outbound(client):
    await client.wait_until_ready()
    while not client.is_closed():
        result = r.brpop(OUTBOUND)
        msg = json.loads(result[1])

        print('dequeuing {}'.format(msg['data']))

        channel = client.get_channel(msg['dst'])
        await channel.send(msg['data'])



if sys.argv[1] == 'r':
    client = ReadClient()
elif sys.argv[1] == 'w':
    client = WriteClient()
    client.loop.create_task(redis_outbound(client))
else:
    print('use r or w as the arg')

client.run(token);
