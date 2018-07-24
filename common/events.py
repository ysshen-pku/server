# -*- coding: GBK -*-
import conf
from header import SimpleHeader

class MsgCSLogin(SimpleHeader):
	def __init__(self, uid = 0, icon = -1):
		super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
		self.appendParam('uid', uid, 'I')
		self.appendParam('icon', icon, 'i')

class MsgSCLogin(SimpleHeader):
	def __init__(self, x = 0, z = 0, hp = 100):
		super(MsgSCLogin, self).__init__(conf.MSG_SC_LOGIN)
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')
		self.appendParam('hp',hp, 'h')

class MsgSCConfirm(SimpleHeader):
	def __init__(self, uid = 0, result = 0):
		super (MsgSCConfirm, self).__init__(conf.MSG_SC_CONFIRM)
		self.appendParam('uid', uid, 'I')
		self.appendParam('result', result, 'i')

class MsgCSMoveto(SimpleHeader):
	def __init__ (self, x = 0, z = 0, ry = 0):
		super (MsgCSMoveto, self).__init__ (conf.MSG_CS_MOVETO)
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')
		self.appendParam('ry',ry,'d')

class MsgSCMoveto(SimpleHeader):
	def __init__ (self, uid = 0, x = 0, z = 0, ry =0):
		super (MsgSCMoveto, self).__init__ (conf.MSG_SC_MOVETO)
		self.appendParam('uid', uid, 'I')
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')
		self.appendParam('ry', ry, 'd')

class MsgSCNewPlayer(SimpleHeader):
	def __init__(self, uid = 0, x= 0, z=0,ry=0):
		super (MsgSCNewPlayer,self).__init__(conf.MSG_SC_NEWPLAYER)
		self.appendParam('uid',uid,'I')
		self.appendParam('x',x,'d')
		self.appendParam('z', z, 'd')
		self.appendParam('ry', ry, 'd')

class MsgSCNewMonster(SimpleHeader):
	def __init__(self, mid = 0, x = 0, z = 0):
		super (MsgSCNewPlayer,self).__init__(conf.MSG_SC_NEWMONSTER)
		self.appendParam('mid',mid,'I')
		self.appendParam('x',x,'d')
		self.appendParam('z',z,'d')

class MsgSCMonsterMove(SimpleHeader):
	def __init__ (self, mid = 0, x = 0, z = 0):
		super (MsgSCMonsterMove, self).__init__ (conf.MSG_SC_MONSTER_MOVE)
		self.appendParam('mid', mid, 'I')
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')

class MsgCSTrapPlace(SimpleHeader):
	def __init__(self, uid =0, type = 0, x = 0, z =0 ):
		super(MsgCSTrapPlace,self).__init__(conf.MSG_CS_TRAPPLACE)
		self.appendParam('uid',uid,'I')
		self.appendParam('type',type, 'H')
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')

class MsgSCTrapPlace(SimpleHeader):
	def __init__(self,tid = 0, type = 0, x = 0, z= 0):
		super(MsgSCTrapPlace,self).__init__(conf.MSG_SC_TRAPPLACE)
		self.appendParam('tid',tid,'I')
		self.appendParam('type', type, 'H')
		self.appendParam('x', x, 'd')
		self.appendParam('z', z, 'd')

class MsgSCMonsterState(SimpleHeader):
	def __init__(self, mid = 0, hp = 0, state = 0 ):
		super(MsgSCMonsterState,self).__init__(conf.MSG_SC_MONSTER_STATE)
		self.appendParam('mid',mid,'I')
		self.appendParam('hp',hp,'h')
		self.appendParam('state',state,'H')

class MsgCSMonsterDamage(SimpleHeader):
	def __init__(self, uid = 0, mid = 0, damage = 0, stun = 0, range = 0, cx = 0, cz =0):
		super(MsgCSMonsterDamage,self).__init__(conf.MSG_CS_MONSTER_DAMAGE)
		self.appendParam('uid',uid,'I')
		self.appendParam('mid', mid, 'I')
		self.appendParam('damage', damage, 'H')
		self.appendParam('stun', stun, 'h')
		self.appendParam('range',range,'H')
		self.appendParam('cx',cx,'d')
		self.appendParam('cz',cz, 'd')

class MsgSCPlayerInfo(SimpleHeader):
	def __init__(self, uid =0 , hp = 0, coin = 0, exp = 0):
		super(MsgSCPlayerInfo,self).__init__(conf.MSG_SC_PLAYER_INFO)
		self.appendParam('uid',uid,'I')
		self.appendParam('hp',hp,'h')
		self.appendParam('coin',coin,'i')
		self.appendParam('exp',exp,'i')

class MsgSCMonsterDeath(SimpleHeader):
	def __init__(self, uid = 0, mid = 0):
		super(MsgSCMonsterDeath,self).__init__(conf.MSG_SC_MONSTER_DEATH)
		self.appendParam('uid',uid,'I')
		self.appendParam('mid',mid,'I')
