#-*- coding: utf-8 -*-
""" This script contains client and message objects to use the lcddaemon.
"""

import socket
import json

class LCDMessage(object):
    """ This object represents a LCDMessage to send to the LCDDaemon.
    """
    def __init__(self, sender, contents, ttl=60, duration=10, repeat=1):
        self.sender =  sender
        self.contents = contents
        self.ttl = ttl
        self.duration = duration
        self.repeat = repeat
        self.other_args_dict = {}

    def as_dict(self):
        """ Return instance variables of this object and keys of other_args_dict
            in a single dict.
        """
        d =  {'sender': self.sender,
              'contents': self.contents,
              'ttl': self.ttl,
              'duration': self.duration,
              'repeat': self.repeat}
        d.update(self.other_args_dict)
        return d

class LCDClient(object):
    """ This object represents a client for the lcddaemon.
    """
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def sendMessage(self, lcd_message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server, self.port))
        s.sendall(bytes(json.dumps(lcd_message.as_dict())+"\r\n", 'UTF-8'))
        data = s.recv(1024)
        s.close()
        return json.loads(str(data, 'UTF-8'))

if __name__ == '__main__':
    # Here is a little example.
    ip = '127.0.0.1'
    port = 4242
    msg = LCDMessage('Python', 'Hello from Python :)!')
    client = LCDClient(ip, port)
    # This will send the message and print a dict that contains the response
    # message and its code.
    print(client.sendMessage(msg))
