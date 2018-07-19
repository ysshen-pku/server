
import json

# game scence data and manager

class ScenceManager(object):

    def __init__(self):
        # self.mapinfo = bool [][]
        # uid - playerinfo
        # playerinfo { 'Px','Py','Pz', 'Rx', 'Ry', 'Rz'
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

    def updataPlayerInfo(self, playerid, playerinfo):
        if playerid not in self.playerList:
            return False
        else:
            self.playerList[playerid] = playerinfo
            return True

    def updateMonsterInfo(self, monsterid, monsterinfo):
        if monsterid not in self.monsterList:
            return False
        else:
            self.monsterList[monsterid] = monsterinfo
            return True



    def getSyncInfo(self):
        synclist = [self.playerList, self.monsterList]
        return json.dumps(synclist)



