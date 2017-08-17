#!/usr/bin/python3

import asyncio
import os
import socket
import struct
import json

mylist = ["239.85.30.80", "239.85.11.80", "239.81.41.80", "239.81.31.80", "239.31.181.80", "239.31.180.80", \
          "239.1.178.80", "239.1.177.80", "239.65.209.80", "239.82.14.80", "239.81.40.80", "239.81.17.80", \
          "239.65.11.80", "239.1.103.80", "239.81.25.80", "239.90.40.80", "239.39.44.80", "239.34.46.80", \
          "239.7.48.80", "239.1.53.80", "239.1.24.80", "239.1.78.80", "239.1.13.80", "239.1.3.80",  \
          "239.46.44.80", "239.44.52.80", "239.44.32.80", "239.44.43.80", "239.44.21.80", "239.44.13.80", \
          "239.33.42.80", "239.41.45.80", "239.49.41.80", "239.31.40.80"]

mon = {}


header = """HTTP/1.0 200 OK
Content-Type: application/json

"""


@asyncio.coroutine
def my_coroutine(task_name, t):
    yield from asyncio.sleep(0)
    print('{0} is finished'.format(task_name))
 


@asyncio.coroutine
def mcastListen(task_name, group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    mreq = struct.pack("=4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    yield from asyncio.sleep(0)
    while True:
      data = sock.recv(10240).decode()
      d = json.loads(data)
      if 'NL' in d['C']:
          mon[d['C']] = d    
      yield from asyncio.sleep(0)


class Server(asyncio.Protocol):
    def connection_lost(self, exc):
        self.transport.close()

    def connection_made(self, transport):
        self.transport = transport
        self.reporter = transport.get_extra_info('peername')[0]

    def data_received(self, data):
        global mon
        self.out = header + json.dumps(mon, indent=4, sort_keys=True) + '\n'
        self.transport.write(self.out.encode())
        self.transport.close()
        return
 

if __name__ == '__main__':
    tasks = []
    for c, i in enumerate(mylist):
        tasks.append(mcastListen(c,i,9091))
 
    loop = asyncio.get_event_loop()

    coro = loop.create_server(Server, '0.0.0.0', 5000)
    server = loop.run_until_complete(coro)
    print('Listing on {}'.format(server.sockets[0].getsockname()))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
