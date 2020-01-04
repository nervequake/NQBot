#!/usr/bin/python3
from utils import *

q = Queue()
while True:
    msg = q.get(Queue.INBOUND)
    if msg['data'] == 'ping':
        out = {
            'data': 'pong',
            'ctx': msg['ctx']
        }
        q.add(Queue.OUTBOUND, out)
