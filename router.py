#!/usr/bin/python3
import time

from utils import *

p = PubSub()
p.sub(PubSub.COMMAND)

while True:
    chan, msg = p.get()
    
    if msg:
        if msg['data'] == 'ping':
            out = {
                'act': 'send',
                'data': 'pong',
                'ctx': msg['ctx']
            }
            p.pub(PubSub.SMPLCMD, out)
    time.sleep(0.01)