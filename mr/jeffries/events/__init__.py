from zope.component import getGlobalSiteManager
from zope.interface import implements

from interfaces import IEvent, IErrorLogEvent

def initialize(context):
    from errorlog import ErrorLogEventAdapter
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(ErrorLogEventAdapter, (IErrorLogEvent,),
                        IEvent, 'errorlog')

class BaseEventAdapter(object):
    implements(IEvent)

    def __init__(self, event, **kwargs):
        raise NotImplementedError()