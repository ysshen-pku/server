# -*- coding: gbk -*-
#File:handler.py
#Desc:Unity3D work: FPS Game Server side MessageHandler
#Author: ysshen

import threading
import random
import json
from time import time
from userdata import UserData
from scence import ScenceManager
import conf
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

	#register handler
	def _register(self,username,pwd):
		#print username,pwd
		reDict = {'MsgT': conf.REGISTER_RESPONSE}
		if username in self.data.users:
			reDict['S'] = conf.AlreadyExistence
			return  conf.SERVER_SEND_RESPONSE,reDict
		posx = random.uniform(0,5)
		if random.randint(0,1) == 0:
			posx *= -1
		info = {'pos':{'x':posx,'y':0,'z':0},'rot':{'x':0,'y':0,'z':0},'s':0}
		self.data._adduser(username,pwd,info)
		# userinfo = self.data.users[username]
		# self.scenceManager.newPlayerIn(username, userinfo)
		reDict['S'] = conf.RegisterSuccessfully
		# reDict.update(userinfo)
		return conf.SERVER_SEND_RESPONSE,reDict

	#login handler
	def _login(self,uid,username,pwd):
		reDict = {'MsgT':conf.LOGIN_RESPONSE}
		if username not in self.data.users:
			reDict['S']=conf.UncorrectUsername
			return conf.SERVER_SEND_RESPONSE,reDict
		if pwd != self.data.users[username]['password']:
			reDict['S'] = conf.UncorrectPassword
			return conf.SERVER_SEND_RESPONSE,reDict
		else:
			#print 'login:'+username+pwd
			if username in self.onlineSocks.items():
				reDict['S'] = conf.UserAlreadyOnline
				return conf.SERVER_SEND_RESPONSE,reDict
			reDict['S'] = conf.LoginSuccessfully
			self.onlineUsers[uid] = username
			userinfo = self.data.users[self.name]
			# self.scenceManager.newPlayerIn(username, userinfo)
			reDict.update(userinfo)
			#print r_msg
			return conf.SERVER_SEND_RESPONSE,reDict

	# main handle func, analyse message
	def _handle(self,uid, msg):
		reqst = json.loads(msg)
		if reqst['MsgT'] == conf.LOGIN_REQST:
			name, pwd = reqst['UserName'],reqst['Password']
			return conf.LOGIN_RESPONSE,self._login(uid,name,pwd)
		elif reqst['MsgT'] == conf.REGISTER_REQST:
			name, pwd = reqst['UserName'],reqst['Password']
			return conf.REGISTER_RESPONSE, self._register(name,pwd)
		elif reqst['MsgT'] == conf.EVENT_REQST:
			reqst.pop('MsgT')
			return conf.EVENT_RESPONSE, reqst

	def _eventHandler(self,uid, reqst):
		rtype = reqst.pop('EvtT')
		if rtype == conf.EVENT_SYNC_REQST:
			return reqst
		else:
			pass


	#spawn enemy in client side
	def spawnEnemy(self):
		pass

	# sync game player data from client side
	def _updateInfo(self,health,ammo):
		if self.name:
			if health<=0:
				self.data._updatehp(100)
			else:
				self.data._updatehp(health)
			self.data._updateammo(ammo)
			self._update()

	# update database
	def _update(self,name):
		if name in self.data.users:
			self.data._dump()

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