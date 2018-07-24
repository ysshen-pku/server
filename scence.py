import sys
sys.path.append('./common')
import json
import conf
import math
from events import *
from collections import deque
# game scence data and manager

class ScenceManager(object):

    def __init__(self):
        # self.mapinfo = bool [][]
        # uid - playerinfo
        # playerinfo { 'x','z',  'Ry',
        # 'HP', 'State', ..?}
        self.playerList = {}
        # monsterinfo { 'x','z',  'Ry',
        # 'HP', 'State',
        self.monsterList = {}
        self.trapList = {}
        self.currMosterId = 0
        self.currTrapId = 0
        self.mapInfo = [[] for i in xrange(100)]
        self.readMapInfo()

    def readMapInfo(self):
        with open("./mapinfo",'r') as mapfile:
            i = 0
            for line in mapfile:
                line = line[1:-1]
                nums = line.split(',')
                for j in xrange(conf.MAP_SIZE_X):
                    self.mapInfo[i].append(nums[j])
                i += 1

    def newPlayerIn(self, playerid, x, z):
        if playerid in self.playerList:
            return None
        else:
            info = {'x':x,'z':z,'y':0,'uid':playerid,'hp':100,'coin':0,'exp':0}
            self.playerList[playerid] = info
            return info

    def newMonster(self):
        self.currMosterId += 1
        x,z = conf.MONSTER_SPAWN_POINT
        info = {'x': x, 'y': 0, 'z': z, 'mid': self.currMosterId, 'hp':100, 'state':conf.MONSTER_STATE_MOVE}
        self.monsterList[self.currMosterId] = info
        return info

    def addTrap(self, type, x, z):
        for trapinfo in self.trapList.itervalues():
            if abs(x-trapinfo['x'])<conf.TRAP_RANGE or abs(z-trapinfo['z'])<conf.TRAP_RANGE:
                return False
        self.currTrapId += 1
        info = {'tid':self.currTrapId, 'type':type, 'x':x, 'z':z}
        self.trapList[self.currTrapId] = info
        print self.currTrapId
        return True
    # stun 0:nothing        1: stun the monster
    # range 0: damage mid   1: damage all in range point with (cx,cz)
    # return death mids for msg
    def handleDamage(self,uid, mid, damage, stun, range, cx, cz):
        # return list with changed monsters
        monsters = []
        if range == 0:
            if self.monsterList.has_key(mid):
                tmp = self._dealDamage(uid,mid,damage,stun)
                if tmp:
                    monsters.append(tmp)
            else:
                print 'trying to damage a non-exist monster'
                return None
        else:
            if self.monsterList:
            # deal range damage
                for monsterinfo in self.monsterList.itervalues():
                    if math.hypot(cx-monsterinfo['x'],cz-monsterinfo['z']) < range:
                        tmp = self._dealDamage(uid,monsterinfo['mid'],damage,stun)
                        if tmp:
                            monsters.append(tmp)
        return monsters

    def _dealDamage(self,uid, mid, damage, stun):
        if self.monsterList[mid]['hp'] < damage:
            # if death todo------------
            self.monsterList.pop(mid)
            self.playerList[uid]['coin'] += conf.MONSTER_DEATH_COIN
            self.playerList[uid]['exp'] += conf.MONSTER_DEATH_EXP
            return mid
        else:
            self.monsterList[mid]['hp'] -= damage
            if stun:
                self.monsterList[mid]['state'] = conf.MONSTER_STATE_IDLE
            return None


    def getTrapInfos(self):
        return self.trapList.values()

    def _getOtherPlayerInfos(self,uid):
        others = []
        for playerinfo in self.playerList.itervalues():
            if playerinfo['uid'] != uid:
                others.append(playerinfo)
        return others

    def playerLeave(self, playerid):
        if playerid in self.playerList:
            return False
        else:
            self.playerList.pop(playerid)
            return True

    def _playerMove(self, playerid, x, z,ry):
        if self.playerList.has_key(playerid):
            self.playerList[playerid]['x']=x
            self.playerList[playerid]['z']=z
            self.playerList[playerid]['ry']=ry
            head = MsgSCMoveto(playerid,x,z,ry)
            return head.marshal()
        else:
            return None

    def getOtherPlayers(self, uid):
        others = []
        if self.playerList:
            for playerid in self.playerList.iterkeys():
                if playerid !=uid:
                    others.append(playerid)
        return others

    def getMonsterDes(self,mid):
        aimpos = conf.MONSTER_DESTINATION
        info = self.monsterList[mid]
        if self.playerList:
            mindistance = conf.MONSTER_CHASE_RANGE + 1
            for player in self.playerList.itervalues():
                distance = math.hypot(info['x']-player['x'],info['z']-player['z'])
                if distance < mindistance:
                    aimpos = (player['x'],player['z'])
                    mindistance = distance
        return aimpos




    # def _tryMoveto(self, name, pos2D):

def main():
    scene = ScenceManager()


if __name__ == "__main__":
    main()





