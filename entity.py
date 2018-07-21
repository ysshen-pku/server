
import conf
import logging
from simpleHost import SimpleHost
from handler import MessageHandler
from scence import ScenceManager
from userdata import UserData

# entities:
# remoteplayer
# monster
# trap

class Entity(object):

    def __init__(self):
        self.id = -1
        self.type = conf.ENTITY_PLAYER
        self.info = {}

    def _updatePosition(self,pos):
        self.position = pos




