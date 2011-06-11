'''
Created on Jun 10, 2011

@author: mitch
'''
from zope.interface import Interface

class IMonitorTool(Interface):
    def notify(self, listener, event):
        pass