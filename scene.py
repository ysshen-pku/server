import sys
sys.path.append('./common')
import json
import conf
import math
import time
from events import *
from collections import deque
# game scence data and manager

class SceneManager(object):

    def __init__(self):
        self.mapInfo = [[] for i in xrange(180)]
        self.readMapInfo()
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
        self.monsterSpeed = conf.MONSTER_SPEED_WALK
        self.time = time.time()

    def readMapInfo(self):
        with open("./mapinfo.txt",'r') as mapfile:
            i = 0
            for line in mapfile:
                line = line[1:-1]
                nums = line.split(',')
                for j in xrange(conf.MAP_SIZE_X):
                    self.mapInfo[i].append(nums[j])
                # print self.mapInfo[i]
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
        x,z = conf.MONSTER_DESTINATION
        des = {'x':x, 'z':z}
        ax, az =conf.MONSTER_SPAWN_POINT
        x = -10 + ax * conf.MAP_ACCURATE
        z = 35 - az * conf.MAP_ACCURATE
        info = {'x': x, 'y': 0, 'z': z,'ax':ax, 'az':az,'des':des, 'mid': self.currMosterId, 'hp':100, 'state':conf.MONSTER_STATE_MOVE}
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
                # print 'trying to damage a non-exist monster'
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

    def getMonsterPos(self, mid):
        info = self.monsterList[mid]
        if self.playerList:
            mindistance = conf.MONSTER_CHASE_RANGE + 1
            despos = None
            for player in self.playerList.itervalues():
                distance = math.hypot(info['x']-player['x'],info['z']-player['z'])
                if distance < mindistance:
                    despos = self._getArrayPos(player['x'],player['z'])
                    print player['x'],player['z']
                    print despos
                    mindistance = distance
            if despos:
                self.monsterList[mid]['des']={'x':despos[0],'z':despos[1]}
        self._monsterMove(mid)
        return self.monsterList[mid]['x'],self.monsterList[mid]['z']

    # change position to fixed pos
    def _getArrayPos(self,x,z):
        if x<conf.MAP_EDGE_X or z>conf.MAP_EDGE_Z:
            return None,None
        return int(10*(x-conf.MAP_EDGE_X)/3),int(10*(conf.MAP_EDGE_Z-z)/3)

    # should be call every 0.1s
    def _monsterMove(self, mid):
        monster = self.monsterList[mid]
        ax,az = monster['ax'],monster['az']
        des = monster['des']
        if des['z'] == az and des['x']==ax:
            return False
        elif des['z'] > az and az+1<conf.MAP_SIZE_Z and self.mapInfo[az+1][ax]:
            # move down
            monster['az'] += 1
            monster['z'] -=0.3
        elif des['z'] <az and az-1 >-1 and self.mapInfo[az-1][ax]:
            monster['az'] -= 1
            monster['z'] += 0.3
        elif des['x'] > ax and ax+1<conf.MAP_SIZE_X and self.mapInfo[az][ax+1]:
            monster['ax'] += 1
            monster['x'] += 0.3
        elif des['x'] < ax and ax-1 >-1 and self.mapInfo[az][ax-1]:
            monster['ax'] -= 1
            monster['x'] -= 0.3
        else:
            return False
        # print monster['ax'],monster['az'],monster['des']
        return True





    # def _tryMoveto(self, name, pos2D):

def main():
    scene = SceneManager()


if __name__ == "__main__":
    main()





