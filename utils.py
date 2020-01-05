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

class PubSub:
    # events
    MESSAGE = 'event:message'
    COMMAND = 'event:command'

    # simple interface for sending commands to the bot. eg send message to channel
    SMPLCMD = 'command:simple'

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()

    def pub(self, channel, msg):
        serialized = json.dumps(msg)
        self.r.publish(channel, serialized)

    def sub(self, channel):
        self.p.subscribe(channel)

    def get(self):
        message = self.p.get_message()
        if message == None:
            return None, None
        if message['type'] != 'message':
            return None, None

        return message['channel'].decode('utf-8'), json.loads(message['data'])

