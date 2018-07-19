# -*- coding: utf-8 -*-
#File:handler.py
#Desc:Unity3D work: FPS Game Server side MessageHandler
#Author: ysshen

import threading
import random
import json
import conf
from time import time
from userdata import UserData
from scence import ScenceManager
import conf


class MessageHandler(object):

	#data: Database class
	#socket: handler owner; name: owner username
	#online: whether game user is onlined 
	def __init__(self):
		self.data = UserData()
		self.scenceManager = ScenceManager()
		# sock: username
		self.onlineSocks = {}

	#register handler
	def _register(self,username,pwd):
		#print username,pwd
		reDict = {'MessageType': conf.REGISTER_RESPONSE}
		if username in self.data.users:
			reDict['State'] = conf.AlreadyExistence
			return  json.dumps(reDict)
		self.data._adduser(username,pwd,0)
		userinfo = self.data.users[username]
		# self.scenceManager.newPlayerIn(username, userinfo)
		reDict['State'] = conf.RegisterSuccessfully
		# reDict.update(userinfo)
		return json.dumps(reDict)

	#login handler
	def _login(self,sock,username,pwd):
		reDict = {'MessageType':conf.LOGIN_RESPONSE}
		if username not in self.data.users:
			reDict['State']=conf.UncorrectUsername
			return json.dumps(reDict)
		if pwd != self.data.users[username]['password']:
			reDict['State'] = conf.UncorrectPassword
			return json.dumps(reDict)
		else:
			#print 'login:'+username+pwd
			if username in self.onlineSocks.items():
				reDict['State'] = conf.UserAlreadyOnline
				return json.dumps(reDict)
			reDict['State'] = conf.LoginSuccessfully
			self.onlineSocks[sock] = username
			userinfo = self.data.users[self.name]
			self.scenceManager.newPlayerIn(username, userinfo)
			reDict.update(userinfo)
			#print r_msg
			return json.dumps(reDict)

	# main handle func, analyse message
	def _handle(self,msg,sock):
		data = msg.strip()
		#print data
		reqsts = data.split('#')
		for reqst in reqsts:
			#print reqst
			cmd, info = reqst.split('\t',1)
			cmd = cmd.strip()
			if int(cmd) == LOGIN_REQST:
				name,pwd = info.split('\t')
				return self._login(sock,name,pwd)
			elif int(cmd) == REGISTER_REQST:
				#print "cmd==2"
				print info
				name,pwd = info.split('\t')
				#print name,pwd
				return self._register(name,pwd)
			elif int(cmd) == UPDATE_REQST:
				hp,ammo = info.split('\t')
				return self._updateInfo(hp,ammo)
			else:
				return None

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
	def exceptionHandler(self, sock):
		if sock in self.onlineSocks:
			print "{} has disconnected.".format(sock)
			self._update(self.onlineSocks[sock])

def main():
	han= MessageHandler()
	han._login('test','123')

if __name__ == '__main__':
	main()