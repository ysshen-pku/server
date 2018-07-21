# -*- coding: gbk -*-
#File:handler.py
#Desc:Unity3D work: FPS Game Server side MessageHandler
#Author: ysshen
import sys

from common.events import MsgCSLogin

sys.path.append('./common')

import struct
from userdata import UserData
import conf
from events import *
import random

class MessageHandler(object):

	#data: Database class
	#socket: handler owner; name: owner username
	#online: whether game user is onlined
	def __init__(self):
		self.data = UserData()
		# self.scenceManager = ScenceManager()
		# sock: username
		self.onlineUsers = {}

	def _login(self,uid):
		if self.onlineUsers.has_key(uid):
			info = self.onlineUsers[uid]
			return conf.LOGIN_RESPONSE, self.onlineUsers[uid]

	# main handle func, analyse message
	def _handle(self,uid,msg):
		mtype = struct.unpack("H", msg[0:2])
		if mtype == conf.MSG_CS_LOGIN:
			data = MsgCSLogin().unmarshal(msg[2:])
			return self._login(data.uid)



	def _eventHandler(self,uid, reqst):
		rtype = reqst.pop('EvtT')
		if rtype == conf.EVENT_SYNC_REQST:
			return reqst
		else:
			pass


	# disconncetion handler
	def exceptionHandler(self, uid):
		if uid in self.onlineUsers:
			print "{} has disconnected.".format(uid)
			self._update(self.onlineUsers[uid])

def main():
	han= MessageHandler()
	han._login('test','123')

if __name__ == '__main__':
	main()