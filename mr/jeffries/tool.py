'''
Created on Jun 10, 2011

@author: mitch
'''

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from OFS.Folder import Folder
from Products.CMFCore.utils import UniqueObject
from zope.interface import implements

import config
from interfaces import IMonitorTool
from mr.jeffries.dispatchers.interfaces import IDispatcher
from mr.jeffries.listeners.interfaces import IListener

class MonitorTool(Folder, UniqueObject):

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    implements(IMonitorTool)

    id = config.TOOL_NAME
    title = 'mr.jeffries monitoring tool'
    meta_type = 'MonitorTool'

    def notify(self, event):
        # Send events back to listeners
        listeners = self.getListeners()
        relevant_listeners = filter(lambda l: l.event_type==event.type, listeners)
        for l in relevant_listeners:
            l.notify(event)

    def dispatch(self, listener, event):
        # Send events filtered by listeners to dispatchers
        dispatchers = filter(lambda o: IDispatcher.providedBy(o), aq_parent(aq_inner(listener)).objectValues())
        for d in dispatchers:
            d.dispatch(event)

    def getListeners(self):
        return filter(lambda o: IListener.providedBy(o), self.objectValues())

    def initializeHandlers(self):
        for l in self.getListeners():
            l._addHandle()

InitializeClass(MonitorTool)