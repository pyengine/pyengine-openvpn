from pyengine.info import DataInfo
from pyengine.lib.error import *

class DataExampleInfo(DataInfo):

    def __init__(self, data, options):
        super(self.__class__, self).__init__(data, options)

    def __repr__(self):
        return '<DataExampleInfo: %s>' %self.data['id']

    def fetchByData(self):
            self.output['id'] = self.data['id']
