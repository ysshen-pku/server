import sys
sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./common_server')

import conf
from events import *
import logging
import threading
import Queue
from netStream import NetStream
from simpleHost import SimpleHost
from handler import MessageHandler
from scence import ScenceManager

from userdata import UserData

class GameServer(object):

    def __init__(self):
        self.entities = {}
        self.host = SimpleHost()
        self.msgHandler = MessageHandler()
        self.scenceManager = ScenceManager()
        # self.userData = UserData()
        self.msgQueue = Queue.Queue()

    def generateEntityID(self):
        eid = -1
        for i in xrange(len(self.entities)):
            if self.entities[i] == None:
                eid = i
                break
        if eid < 0:
            eid = len(self.entities)
            self.entities.append(None)
        if len(self.entities) >= conf.MAX_ENTITIS_INDEX:
            print "entities number exceed"
        return eid

    #
    def registerEntity(self, entity):
        eid = self.generateEntityID
        entity.id = eid
        self.entities[eid] = entity
        return

    def _start(self, port):
        print 'trying start game...'
        self.host.startup(port)
        while 1:
            self.host.process()

            while True:
                # print '.'
                etype, hid, data = self.host.read()
                # print etype,data
                # message queue empty
                if etype < 0:
                    break
                if etype == conf.NET_CONNECTION_DATA:
                    # handle msg and process
                    state, others = self.msgHandler._handle(hid, data)
                    print state,others
                    if state == conf.LOGIN_RESPONSE:
                        # need todo -------------------------
                        # self.scenemanager.newplayerin
                        self.msgQueue.put_nowait(([hid],others))
                    # response
                    elif state == conf.MOVE_RESPONSE:
                        uid, x, y = others
                        msg = self.scenceManager._playerMove(uid,x,y)
                        if msg:
                            otherPlayers = self.host.clients.remove(uid)
                            if otherPlayers:
                                self.msgQueue.put_nowait((otherPlayers,msg))
                if etype == conf.NET_CONNECTION_NEW:
                    # Todo
                    print 'new connection'
                    # pass

                if etype == conf.NET_CONNECTION_LEAVE:
                    # Todo
                    pass
            self._trySendMsg()
            # sync sever scence to client

    def _trySendMsg(self):
        while not self.msgQueue.empty():
            hids, data = self.msgQueue.get()
            for hid in hids:
                self.host.sendClient(hid,data)


    def _syncSC(self):
        entityq = self.scenceManager._syncPackage()
        while entityq:
            mt, et, info = entityq.pop()

        # for client in self.host.clients:

def main():
    server = GameServer()
    server._start(50010)


if __name__ == '__main__':
    main()




