import sys
sys.path.append('./common')
import json
import conf
import math
import time
from events import *
import astar
from collections import deque
# game scence data and manager

class SceneManager(object):

    def __init__(self):
        self.mapInfo = [[] for i in xrange(conf.MAP_SIZE_Z)]
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
            info = {'x':x,'z':z,'y':0,'uid':playerid,'hp':100,'coin':1000,'exp':0,'spike':0,'freeze':0}
            self.playerList[playerid] = info
            return info

    def newMonster(self):
        self.currMosterId += 1
        x,z = conf.MONSTER_DESTINATION
        des = {'x':x, 'z':z}
        ax, az =conf.MONSTER_SPAWN_POINT
        x = conf.MAP_EDGE_X + ax * conf.MAP_ACCURATE
        z = conf.MAP_EDGE_Z - az * conf.MAP_ACCURATE
        info = {'x': x, 'y': 0, 'z': z,'ax':ax, 'az':az,'des':des,'mid': self.currMosterId,
                'hp':100, 'state':conf.MONSTER_STATE_MOVE, 'speed':conf.MONSTER_SPEED_WALK}
        self.monsterList[self.currMosterId] = info
        return info

    def buyTrap(self, uid, ttype):
        if self.playerList[uid]['coin'] < conf.TRAP_COST:
            return
        self.playerList[uid]['coin'] -= conf.TRAP_COST
        if ttype == 1:
            self.playerList[uid]['spike'] += 1
        elif ttype == 2:
            self.playerList[uid]['freeze'] += 1

    def addTrap(self,uid, type, x, z):
        ax, az = self._getArrayPos(x, z)
        for trapinfo in self.trapList.itervalues():
            if abs(ax-trapinfo['ax'])<conf.TRAP_RANGE or abs(az-trapinfo['az'])<conf.TRAP_RANGE:
                return False
        self.currTrapId += 1
        info = {'uid':uid,'tid':self.currTrapId, 'type':type, 'ax':ax, 'az':az, 'x':x, 'z':z}
        self.trapList[self.currTrapId] = info
        if type == 1:
            self.playerList[uid]['spike'] -= 1
        elif type ==2:
            self.playerList[uid]['freeze'] -= 1
        # print self.currTrapId
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

    def _damagePlayer(self, uid, damage):
        if self.playerList.has_key(uid):
            info = self.playerList[uid]
            # when kill player
            if info['hp'] < damage:
                info['hp'] = 0
                return True
            else:
                info['hp'] -= damage
        return False

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
    # return the next pos in next logic frame for monster
    # first check trap effect, then check state
    # if stay move state, check Destination, and move
    def getMonsterPos(self, mid):
        info = self.monsterList[mid]
        finx, finz = conf.MONSTER_DESTINATION
        if info['ax'] == finx and info['az'] == finz:
            return False, 1,1
        intrap, trapinfo = self._checkTrap(info['ax'],info['az'])
        if intrap == 1:
            if self._dealDamage(trapinfo['uid'], mid, conf.TRAP_SPIKE_DAMAGE, 0):
                return False,0,0
        elif intrap == 2:
            info['speed'] = conf.MONSTER_SPEED_SLOW
        else:
            info['speed'] = conf.MONSTER_SPEED_WALK
        # if info['state'] == conf.MONSTER_STATE_STUN:
        #    return True,info['x'],info['z']
        # check destination
        uid, s = self._findNearestPlayer(info['x'],info['z'])
        if info['state'] == conf.MONSTER_STATE_ATTACK:
            if uid:
                if s == conf.MONSTER_STATE_ATTACK:
                    if self._damagePlayer(uid,1):
                        self.OnplayerDeath()
                        return False,1,0
                elif s == conf.MONSTER_STATE_CHASE:
                    info['state'] = conf.MONSTER_STATE_CHASE
                    info['target'] = uid
            else:
                info['state'] = conf.MONSTER_STATE_MOVE
        elif info['state'] == conf.MONSTER_STATE_CHASE:
            if uid:
                if s == conf.MONSTER_STATE_ATTACK:
                    info['state'] = conf.MONSTER_STATE_ATTACK
                    info['target'] = uid
                elif s == conf.MONSTER_STATE_CHASE:
                    info['target'] = uid
            else:
                info['target'] = None
                info['state'] = conf.MONSTER_STATE_MOVE
        elif info['state'] == conf.MONSTER_STATE_MOVE:
            # if in attack range
            if uid:
                if s == conf.MONSTER_STATE_ATTACK:
                    info['state'] = conf.MONSTER_STATE_ATTACK
                    info['target'] = uid
                elif s == conf.MONSTER_STATE_CHASE:
                    info['state'] = conf.MONSTER_STATE_CHASE
                    info['target'] = uid
            else:
                pass
        self._monsterMove(mid)
        return True,self.monsterList[mid]['x'],self.monsterList[mid]['z']

    def _findNearestPlayer(self,x,z):
        if self.playerList:
            mindistance = conf.MONSTER_CHASE_RANGE
            targetUid = None
            for player in self.playerList.itervalues():
                distance = math.hypot(info['x'] - player['x'], info['z'] - player['z'])
                if distance < mindistance:
                    targetUid = player['uid']
                    mindistance = distance
            if targetUid:
                if mindistance < conf.MONSTER_ATTACK_RANGE:
                    return targetUid, conf.MONSTER_STATE_ATTACK
                else:
                    return targetUid, conf.MONSTER_STATE_CHASE
        return None, 0

    # change position to fixed pos
    def _getArrayPos(self,x,z):
        if x<conf.MAP_EDGE_X or z>conf.MAP_EDGE_Z:
            return None,None
        return int(5*(x-conf.MAP_EDGE_X)),int(5*(conf.MAP_EDGE_Z-z))

    def _checkTrap(self, ax, az):
        for trapinfo in self.trapList.itervalues():
            if abs(trapinfo['ax']-ax) <= 5 and abs(trapinfo['az']-az) <= 5:
                return trapinfo['ttype'], trapinfo
        return 0, None

    # should be call every 0.1s
    def _monsterMove(self, mid):
        monster = self.monsterList[mid]
        ax,az = monster['ax'],monster['az']
        # des[0] == des.ax des[1] == des.az
        des = conf.MONSTER_DESTINATION
        if monster['target']:
            des = self._getArrayPos(self.playerList[monster['target']]['x'],
                                    self.playerList[monster['target']]['z'])
        if des[1] == az and des[0] == ax:
            return False
        if des[1] > az and des[0] >ax:
            if self._touchMapArray(ax+1,az+1):
                ax, az = ax+1,az+1
            elif self._touchMapArray(ax,az+1):
                az +=1
            elif self._touchMapArray(ax+1,az):
                ax +=1
            elif self._touchMapArray(ax-1,az):
                ax -=1
        else:
            return False
        # print monster['ax'],monster['az'],monster['des']
        return True

    def _touchMapArray(self,x, z):
        if 0 <= x < conf.MAP_SIZE_X and 0 <=z <conf.MAP_EDGE_Z:
            return self.mapInfo[z][x]
        return 0



def main():
    scene = SceneManager()
    start = conf.MONSTER_SPAWN_POINT
    end = conf.MONSTER_DESTINATION
    print astar.next_move(start,end,scene.mapInfo)


if __name__ == "__main__":
    main()





