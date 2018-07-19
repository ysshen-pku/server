#
# message package

import json

class Package(object):

    def __init__(self):
        pass
    def unpack(self,jsonData):
        dic = json.loads(jsonData)
        return dic

    def enpack(self,rawDict):
        jmsg = json.dumps(rawDict)
        return jmsg
