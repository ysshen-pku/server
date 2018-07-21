# -*- coding: GBK -*-
import conf
from header import SimpleHeader

class MsgCSLogin(SimpleHeader):
	def __init__(self, uid = 0, icon = -1):
		super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
		self.appendParam('uid', uid, 'I')
		self.appendParam('icon', icon, 'i')

class MsgSCLogin(SimpleHeader):
	def __init__(self, x = 0, y = 0):
		super(MsgSCLogin, self).__init__(conf.MSG_SC_LOGIN)
		self.appendParam('x', x, 'f')
		self.appendParam('y', y, 'f')

class MsgSCConfirm(SimpleHeader):
	def __init__(self, uid = 0, result = 0):
		super (MsgSCConfirm, self).__init__(conf.MSG_SC_CONFIRM)
		self.appendParam('uid', uid, 'I')
		self.appendParam('result', result, 'i')

class MsgCSMoveto(SimpleHeader):
	def __init__ (self, x = 0, y = 0):
		super (MsgCSMoveto, self).__init__ (conf.MSG_CS_MOVETO)
		self.appendParam('x', x, 'f')
		self.appendParam('y', y, 'f')

class MsgSCMoveto(SimpleHeader):
	def __init__ (self, uid = 0, x = 0, y = 0):
		super (MsgSCMoveto, self).__init__ (conf.MSG_SC_MOVETO)
		self.appendParam('uid', uid, 'I')
		self.appendParam('x', x, 'f')
		self.appendParam('y', y, 'f')
