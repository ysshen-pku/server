# coding: GBK
import sys
sys.path.append('./common')

import conf
from events import *
from userdata import UserData
import struct
import logging
import random

class MessageHandler(object):

    def __init__(self):


    def _handle(self,hid,msg):
        mtype = struct.unpack("H",msg[0:2])[0]
        if mtype == conf.MSG_CS_LOGIN:
            data = MsgCSLogin().unmarshal(msg)
            return self._login(hid,data.uid)
        elif mtype == conf.MSG_CS_MOVETO:
            if self.onlines.has_key(hid):
                data = MsgCSMoveto().unmarshal(msg)
                return conf.MOVE_RESPONSE, (self.onlines[hid],data.x,data.z,data.ry)
            else:
                print 'trying move player:'+hid+', yet he is offline.'
        elif mtype == conf.MSG_CS_TRAPPLACE:
            if self.onlines.has_key(hid):
                data = MsgCSTrapPlace().unmarshal(msg)
                return conf.TRAP_RESPONSE, (self.onlines[hid], data.type,data.x,data.z)
            else:
                print 'offline player trying to place trap'
        elif mtype == conf.MSG_CS_MSG_CS_MONSTER_DAMAGE:
            if self.onlines.has_key(hid):
                data = MsgCSMonsterDamage().unmarshal(msg)
                return
        else:
            pass
        return 0,None

    def _login(self,hid,uid):
        if self.data.users.has_key(uid):
            self.onlines[hid]=uid
            userinfo = self.data.users[uid]
            #head = MsgSCLogin(info['pos']['x'],info['pos']['z'])
            #data = head.marshal()
            return conf.LOGIN_RESPONSE, userinfo

    def getPlayeruid(self,hid):
        if self.onlines.has_key(hid):
            return self.onlines[hid]
        else:
            return None

    def getPlayerhid(self,uid):
        hid = None
        if self.onlines:
            for _hid,_uid in self.onlines.iteritems():
                if _uid == uid:
                    return _hid
        return hid



