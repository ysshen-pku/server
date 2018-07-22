
import json
import conf
from events import *
from collections import deque
# game scence data and manager

class ScenceManager(object):

    def __init__(self):
        # self.mapinfo = bool [][]
        # uid - playerinfo
        # playerinfo { 'x','y','z', 'Rx', 'Ry', 'Rz'
        # 'HP', 'State', ..?}
        self.playerList = {}
        # monsterinfo { 'Px','Py','Pz', 'Rx', 'Ry', 'Rz'
        # 'HP', 'State',
        self.monsterList = {}

    def newPlayerIn(self, playerid, x, z):
        if playerid in self.playerList:
            return False
        else:
            info = {'x':x,'z':z,'y':0,'uid':playerid}
            self.playerList[playerid] = info
            return info

    def playerLeave(self, playerid):
        if playerid in self.playerList:
            return False
        else:
            self.playerList.pop(playerid)
            return True

    def _playerMove(self, playerid, x, z):
        if playerid not in self.playerList:
            return None
        else:
            self.playerList[playerid]['x']=x
            self.playerList[playerid]['z']=z
            head = MsgSCMoveto(playerid,x,z)
            return head.marshal()

    def updateMonsterInfo(self, monsterid, monsterinfo):
        if monsterid not in self.monsterList:
            return False
        else:
            self.monsterList[monsterid] = monsterinfo
            return True



    # def _tryMoveto(self, name, pos2D):







