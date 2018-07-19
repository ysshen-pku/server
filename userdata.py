# -*- coding: utf-8 -*-
#File:userdata.py
#Desc:Unity3D work: FPS Game Server side game user database
#Author: ysshen

import os
import sys

class UserData():
	def __init__(self):
		self.userfile='./users.d'
		self.users = {}
		self._load()

	def _dump(self):
		with open(self.userfile,'w') as fout:
			for name,info in self.users.items():
				fout.write(name+'\t'+info['password']+'\t'+str(info['ontime'])+'\t'+str(info['health'])+'\t'+str(info['ammo'])+'\n')

	def _adduser(self,name,pwd,time):
		self.users[name]={'name':name,'password':pwd,'ontime':time,'health':100,'ammo':100}
		self._dump()

	def _updatetime(self,name,addtime):
		self.users[name]['ontime'] += addtime

	def _updatehp(self,name,newhp):
		self.users[name]['health']=newhp
	def _updateammo(self,name,newammo):
		self.users[name]['ammo']=newammo

	def _load(self):
		if not os.path.isfile(self.userfile):
			#os.mknod(self.userfile)
			print('FILE NOT EXIST.')
		with open(self.userfile,'r') as fin:
			for line in fin:
				name,pwd,ontime,hp,ammo=line.split('\t')
				self.users[name]={'password':pwd,'ontime':float(ontime),'health':int(hp),'ammo':int(ammo)}


def main():
	userdata=UserData()

if __name__ == '__main__':
	main()