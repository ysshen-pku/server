
import json
import conf
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

    def newPlayerIn(self, playerid, playerinfo):
        if playerid in self.playerList:
            return False
        else:
            self.playerList[playerid] = playerinfo
            return True

    def playerLeave(self, playerid):
        if playerid in self.playerList:
            return False
        else:
            self.playerList.pop(playerid)
            return True

    def _playerMove(self, playerid, x, y):
        if playerid not in self.playerList:
            return None
        else:
            self.playerList[playerid]['x']=x
            self.playerList[playerid]['y']=y
            head = MsgSCMoveto(playerid,x,y)
            return head.marshal()

    def updateMonsterInfo(self, monsterid, monsterinfo):
        if monsterid not in self.monsterList:
            return False
        else:
            self.monsterList[monsterid] = monsterinfo
            return True



    # def _tryMoveto(self, name, pos2D):







