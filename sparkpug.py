#!/usr/bin/python3

import asyncio
import os
import datetime as dt
import json
import copy
mon = {}

store_path='/tmp/store'
info_seconds = 120

header = """HTTP/1.0 200 OK
Content-Type: application/json

"""

def loadSettings():
    global mon
    if os.path.isfile('sparkpug.json'):
        f = open("sparkpug.json", "r")
        mon = json.load(f)
        f.close()
        print('Settings loaded.')
    return mon

def saveSettings(mon):
    try:
        f = open("sparkpug.json", "w")
        f.write(json.dumps(mon, indent=4, sort_keys=True))
        f.close()
        print('Settings saved.')
    except:
        pass

def store(topic, now, key, val):
    with open(store_path+'/'+now[:10]+'_'+topic+'.log', 'a') as f:
            f.write(now+' '+key+' '+val+'\n')

def itemInit(topic):
    if topic not in mon:
        mon.update({topic : {'enable':'0', 'start':'', 'end':'', 'snooze': '', 'interval':'', 'checkedin':'', 'status':'', 'descr':'','timeout':'', 'reporter':'', 'url1':'', 'url2':'','expected':''}})

def itemUpdateStatus(topic, now, key, val, reporter):
    itemInit(topic)
    mon[topic].update({'checkedin': now, 'status': key, 'descr': val, 'reporter': reporter})
    store(topic, now, key, val)

def itemUpdateParams(topic, now, key, val):
    itemInit(topic)
    mon[topic].update({key: val})
    store(topic, now, key, val)

def getAlerts():
    out  = {}
    for item in mon:
        checkedin = dt.datetime.strptime(mon[item]['checkedin'], "%Y-%m-%d %H:%M:%S")
        now = dt.datetime.today()
        tnow = now.time()
        try:
            enable = int(mon[item]['enable'])
        except:
            enable = 0

        try:
            start = dt.datetime.strptime(mon[item]['start'],'%H:%M').time()
        except:
            start = dt.time.min

        try:
            end = dt.datetime.strptime(mon[item]['end'],'%H:%M').time()
        except:
            end = dt.time.max

        try:
            timeout = int(mon[item]['timeout'])
        except:
            timeout = 86400

        if mon[item]['status'] == 'INFO':
            if (now - checkedin).seconds < info_seconds:
                out[item] = copy.deepcopy(mon[item])

        elif end > tnow and tnow > start and enable == True:
            if mon[item]['status'] in ('WARN','ERROR'):
                out[item] = copy.deepcopy(mon[item])
            elif mon[item]['status'] == 'OK':
                if (now - checkedin).seconds > timeout:
                    out[item] = copy.deepcopy(mon[item])
                    out[item]['status'] = 'STALE'


    out = header + json.dumps(out, indent=4, sort_keys=True) + '\n'
    return out

def getEnabled():
    out  = {}
    for item in mon:
        try:
            enable = int(mon[item]['enable'])
        except:
            enable = 0

        if enable == True:
           out[item] = copy.deepcopy(mon[item])
    out = header + json.dumps(out, indent=4, sort_keys=True) + '\n'
    return out

def getDisabled():
    out  = {}
    for item in mon:
        try:
            enable = int(mon[item]['enable'])
        except:
            enable = 0

        if enable == False:
           out[item] = copy.deepcopy(mon[item])

    out = header + json.dumps(out, indent=4, sort_keys=True) + '\n'
    return out

def getItem(item):
    out  = {}
    out[item] = copy.deepcopy(mon[item])
    out = header + json.dumps(out, indent=4, sort_keys=True) + '\n'
    return out

class Server(asyncio.Protocol):

    def connection_lost(self, exc):
        self.transport.close()

    def connection_made(self, transport):
        self.transport = transport
        self.reporter = transport.get_extra_info('peername')[0]

    def data_received(self, data):
        global mon
        self.now = str(dt.datetime.today())[:19]
        try:
            self.msg = data.decode().strip('\r\n').split(' ', 2)
            self.empty = [''] * (3 - len(self.msg) )
            self.topic, self.key, self.val = self.msg + self.empty
        except:
            self.transport.close()
            return

        if self.key in ['INFO','ERROR','WARN','OK']:
            itemUpdateStatus(self.topic, self.now, self.key, self.val, self.reporter)

        elif self.key in ['enable','start','end','snooze','interval','timeout','descr','url1','url2','expected']:
            itemUpdateParams(self.topic, self.now, self.key, self.val)

        elif self.topic in ['GET']:
            if self.key == '/':
                self.out = getAlerts()
                self.transport.write(self.out.encode())
            elif self.key.strip('/') == 'enabled':
                self.out = getEnabled()
                self.transport.write(self.out.encode())
            elif self.key.strip('/') == 'disabled':
                self.out = getDisabled()
                self.transport.write(self.out.encode())
            elif self.key.strip('/') in mon:
                self.out = getItem(self.key.strip('/'))
                self.transport.write(self.out.encode())
            else:
                try:
                    self.topic, self.key, self.val  = self.key[1:].split('/', 2)
                except:
                    self.out = header + json.dumps({'status': 'error'}, indent=4, sort_keys=True) + '\n'
                    self.transport.write(self.out.encode())
                    self.transport.close()
                    return

                if self.topic in mon:
                    if self.key in ['enable','start','end','snooze','interval','timeout','descr','url1','url2','expected']:
                        itemUpdateParams(self.topic, self.now, self.key, self.val)
                        self.out = header + json.dumps({'status': 'ok'}, indent=4, sort_keys=True) + '\n'
                        self.transport.write(self.out.encode())

                    elif self.key in ['INFO','ERROR','WARN','OK']:
                        itemUpdateStatus(self.topic, self.now, self.key, self.val, self.reporter)
                        self.out = header + json.dumps({'status': 'ok'}, indent=4, sort_keys=True) + '\n'
                        self.transport.write(self.out.encode())
                    else:
                        self.out = header + json.dumps({'status': 'error'}, indent=4, sort_keys=True) + '\n'
                        self.transport.write(self.out.encode())
                else:
                    self.out = header + json.dumps({'status': 'error'}, indent=4, sort_keys=True) + '\n'
                    self.transport.write(self.out.encode())
        self.transport.close()

if __name__ == '__main__':
    mon = loadSettings()
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, '0.0.0.0', 5000)
    server = loop.run_until_complete(coro)
    print('Listing on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        saveSettings(mon)
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
