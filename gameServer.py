import sys
sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./common_server')

import conf
from events import *
import logging
import threading
import Queue
import time
import struct
from timer import TimerManager
from netStream import NetStream
from simpleHost import SimpleHost
from scene import SceneManager

from userdata import UserData

class GameServer(object):

    def __init__(self):
        self.playerHids = []
        self.host = SimpleHost()
        self.data = UserData()
        self.sceneManager = SceneManager()
        self.msgQueue = Queue.Queue()
        self.onlines = {}
        self.online = False
        self.monsterNums = 0

    def _start(self, port):
        print 'trying start game...'
        self.host.startup(port)
        ticktimer = TimerManager.addRepeatTimer(0.02,self._tick)
        spawntimer = TimerManager.addRepeatTimer(1.0,self._spawnMonster)
        monstertimer = TimerManager.addRepeatTimer(0.1,self._monsterMove)
        sendtimer = TimerManager.addRepeatTimer(0.01,self._trySendMsg)
        synctimer = TimerManager.addRepeatTimer(0.03,self._syncPlayers)
        trapsyncer = TimerManager.addRepeatTimer(0.05,self._syncTraps)
        monsterstate = TimerManager.addRepeatTimer(0.05,self._syncMonster)
        count = 1
        while True:
            time.sleep(0.005)
            TimerManager.scheduler()
            if self.monsterNums> conf.MONSTER_NUM_ROUND1:
                TimerManager.cancel(spawntimer)
            count += 1

    def _tick(self):
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
                self._handle(hid, data)
            if etype == conf.NET_CONNECTION_NEW:
                # Todo
                print 'new connection'
                # pass
            if etype == conf.NET_CONNECTION_LEAVE:
                # Todo
                if self.onlines.has_key(hid):
                    self.playerHids.remove(hid)
                    self.onlines.pop(hid)
                if not self.playerHids:
                    self.online = False

    def _handle(self,hid,msg):
        mtype = struct.unpack("H",msg[0:2])[0]
        if mtype == conf.MSG_CS_LOGIN:
            data = MsgCSLogin().unmarshal(msg)
            self._login(hid,data.uid)
        elif mtype == conf.MSG_CS_MOVETO:
            if self.onlines.has_key(hid):
                data = MsgCSMoveto().unmarshal(msg)
                self.sceneManager._playerMove(self.onlines[hid],data.x,data.z,data.ry)
            else:
                print 'trying move player:'+str(hid)+', yet he is offline.'
        elif mtype == conf.MSG_CS_TRAPPLACE:
            if self.onlines.has_key(hid):
                data = MsgCSTrapPlace().unmarshal(msg)
                if self.sceneManager.addTrap(data.type,data.x,data.z):
                    # todo ---in scene- change hid coin
                    pass
            else:
                print 'offline player trying to place trap'
        elif mtype == conf.MSG_CS_MONSTER_DAMAGE:
            if self.onlines.has_key(hid):
                data = MsgCSMonsterDamage().unmarshal(msg)
                deadmids = self.sceneManager.handleDamage(data.uid,data.mid,data.damage,data.stun,data.range,data.cx,data.cz)
                self._syncMonster()
                if deadmids:
                    for mid in deadmids:
                    # monster death send msg to destroy
                        head1 = MsgSCMonsterDeath(data.uid, mid)
                        self.msgQueue.put_nowait(([hid],head1.marshal()))
                    self._syncPlayerInfo(hid,self.onlines[hid])
        else:
            pass

    def _login(self,hid,uid):
        if self.data.users.has_key(uid):
            self.onlines[hid]=uid
            info = self.data.users[uid]
            info = info['info']
            head = MsgSCGameStart(info['pos']['x'],info['pos']['z'])
            data = head.marshal()
            self.msgQueue.put_nowait(([hid], data))
            self.playerHids.append(hid)
            self.sceneManager.newPlayerIn(uid, info['pos']['x'], info['pos']['z'])
            self.online = True

    def _getPlayerhid(self,uid):
        hid = None
        if self.onlines:
            for _hid,_uid in self.onlines.iteritems():
                if _uid == uid:
                    return _hid
        return hid

    def _getOtherPlayerHids(self,hid):
        hids = []
        for thishid in self.playerHids:
            if hid != thishid:
                hids.append(thishid)
        return hids

    def _trySendMsg(self):
        while not self.msgQueue.empty():
            hids, data = self.msgQueue.get()
            # print hids,data
            if hids:
                for hid in hids:
                    self.host.sendClient(hid,data)

    def _spawnMonster(self):
        if self.online:
            info = self.sceneManager.newMonster()
            head = MsgSCMonsterMove(info['mid'],info['x'],info['z'])
            self.msgQueue.put((self.playerHids,head.marshal()))
            self.monsterNums += 1


    def _monsterMove(self):
        if self.online:
            if self.sceneManager.monsterList:
                for monster in self.sceneManager.monsterList.itervalues():
                    aimpos = self.sceneManager.getMonsterPos(monster['mid'])
                    #print aimpos
                    head = MsgSCMonsterMove(monster['mid'],aimpos[0],aimpos[1])
                    self.msgQueue.put((self.playerHids,head.marshal()))

    def _syncMonster(self):
        if self.online:
            if self.sceneManager.monsterList:
                for monster in self.sceneManager.monsterList.itervalues():
                    head = MsgSCMonsterState(monster['mid'],monster['hp'],monster['state'])
                    self.msgQueue.put((self.playerHids,head.marshal()))

    # send other players position to every player
    # todo ------------- hid -> client --done
    def _syncPlayers(self):
        if self.playerHids:
            for hid in self.playerHids:
                uid = self.onlines[hid]
                playerinfos = self.sceneManager._getOtherPlayerInfos(uid)
                for playerinfo in playerinfos:
                    head = MsgSCMoveto(playerinfo['uid'],playerinfo['x'],playerinfo['z'])
                    self.msgQueue.put_nowait(([hid], head.marshal()))

    def _syncPlayerInfo(self, hid, uid):
        if hid == None:
            hid = self._getPlayerhid(uid)
        info = self.sceneManager.playerList[uid]
        head = MsgSCPlayerInfo(uid,info['hp'],info['coin'],info['exp'])
        self.msgQueue.put_nowait(([hid], head.marshal()))


    def _syncTraps(self):
        if self.playerHids:
            for hid in self.playerHids:
                trapinfos = self.sceneManager.getTrapInfos()
                for trap in trapinfos:
                    head = MsgSCTrapPlace(trap['tid'], trap['type'], trap['x'], trap['z'])
                    self.msgQueue.put_nowait(([hid], head.marshal()))


        # for client in self.host.clients:

def main():
    server = GameServer()
    server._start(50010)


if __name__ == '__main__':
    main()




