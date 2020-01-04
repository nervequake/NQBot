import redis
import json

def get_token():
    token = ''
    with open('token', 'r') as tk:
        token = tk.read().strip()
    return token

class Queue:
    #messages pending processing
    INBOUND = 'inbound'
    #responses pending sending
    OUTBOUND = 'outbound'

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def add(self, channel, msg):
        serialized = json.dumps(msg)
        self.r.lpush(channel, serialized)

    def get(self, channel):
        result = self.r.brpop(channel)
        msg = json.loads(result[1])
        return msg

