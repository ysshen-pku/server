# -*- coding: GBK -*-

#s2c message type
LOGIN_RESPONSE = 1
REGISTER_RESPONSE = 2
MOVE_RESPONSE = 3

#c2s message type
LOGIN_REQST = 1
REGISTER_REQST = 2
GAMESTART_REQST = 3
EVENT_REQST = 4

# c2s event type
EVENT_MOVE_REQST = 1
EVENT_DAMAGE_REQST = 2
EVENT_SYNC_REQST = 3

# s2c event type
EVENT_MOVE_SC = 1


#state list
RegisterSuccessfully = 0
AlreadyExistence = 1
LoginSuccessfully = 0
UncorrectPassword = 1
UncorrectUsername = 2
UserAlreadyOnline = 3

SERVER_SEND_RESPONSE = 1
SERVER_SEND_BROADCAST = 2

# Cmd Type
CMD_UPDATE_PLAYER = 1

# player states
PLAYER_STATE_IDLE = 1
PLAYER_STATE_MOVE = 2
PLAYER_STATE_DEAD = 3

# monster states
MONSTER_STATE_IDLE = 1
MONSTER_STATE_MOVE = 2
MONSTER_STATE_DEAD = 3

# ENTITY_TYPE

ENTITY_PLAYER = 1
ENTITY_MONSTER = 2

MSG_SC_UPDATE = 1

MSG_CS_LOGIN	= 0x1001
MSG_SC_LOGIN    = 0x2001
# MSG_SC_CONFIRM	= 0x2001
MSG_SC_NEWPLAYER = 0x2003
MSG_CS_MOVETO	= 0x1002
MSG_SC_MOVETO	= 0x2002

NET_STATE_STOP	= 0				# state: init value
NET_STATE_CONNECTING	= 1		# state: connecting
NET_STATE_ESTABLISHED	= 2		# state: connected

NET_HEAD_LENGTH_SIZE	= 4		# 4 bytes little endian (x86)
NET_HEAD_LENGTH_FORMAT	= '<I'

NET_CONNECTION_NEW	= 0	# new connection
NET_CONNECTION_LEAVE	= 1	# lost connection
NET_CONNECTION_DATA	= 2	# data comming

NET_HOST_DEFAULT_TIMEOUT	= 70

MAX_HOST_CLIENTS_INDEX	= 0xffff
MAX_HOST_CLIENTS_BYTES	= 16

MAX_ENTITIS_INDEX = 0xffff
MAX_ENTITIS_BYTES = 16
