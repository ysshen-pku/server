# -*- coding: GBK -*-
#File:userdata.py
#Desc:Unity3D work: FPS Game Server side game user database
#Author: ysshen

import os
import sys
import random
import json
import time

class UserData():
	def __init__(self):
		self.userfile='./users.d'
		self.users = {}
		self._load()

	def _dump(self):
		with open(self.userfile,'w') as fout:
			for user, info in self.users.iteritems():
				# print "memory userinfo"
				# print user, info['info']
				infoJson = json.dumps(info['info'])
				# print "info to Json"
				# print infoJson
				fout.write(str(info['uid']))
				fout.write('\t'+info['pass']+'\t'+infoJson+'\n')

	def _adduser(self,uid,pwd,info):
		self.users[uid]={'uid':uid,'pass':pwd,'info':info}
		# self._dump()

	def _clear(self):
		os.remove(self.userfile)

	def _load(self):
		if not os.path.isfile(self.userfile):
			#os.mknod(self.userfile)
			with open(self.userfile,'w') :
				pass
		with open(self.userfile,'r') as fin:
			for line in fin:
				uid,pwd,infoJson=line.split('\t')
				# print infoJson
				info = json.loads(infoJson)
				# print info
				self.users[int(uid)]={'uid':int(uid),'pass':pwd,'info':info}


def main():
	random.seed(time.time())
	data=UserData()
#	posx = random.uniform(0, 5)
#	if random.randint(0, 1) == 0:
#		posx *= -#1
	posx = 1
	tmpinfo = {'pos': {'x': posx, 'y': 0, 'z': 0}, 'rot': {'x': 0,'y': 0, 'z': 0}, 's': 0}
	data._adduser(1,'123',tmpinfo)
#	posx = random.uniform(0, 5)
#	if random.randint(0, 1) == 0:
#		posx *= -#1
	posx = -1
	tmpinfo = {'pos': {'x': posx, 'y': 0, 'z': 0}, 'rot': {'x': 0,'y': 0, 'z': 0}, 's': 0}
	tmpinfo['pos'][u'x'] = posx
	data._adduser(2, '123', tmpinfo)
	posx = random.uniform(0, 5)
	if random.randint(0, 1) == 0:
		posx *= -1
	tmpinfo = {'pos': {'x': posx, 'y': 0, 'z': 0}, 'rot': {'x': 0, 'y': 0, 'z': 0}, 's': 0}
	tmpinfo['pos'][u'x'] = posx
	data._adduser(3, '123', tmpinfo)

	data._dump()


if __name__ == '__main__':
	main()