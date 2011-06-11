from AccessControl import ClassSecurityInfo
try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import ContentInit
from zope.interface import implements

from mr.jeffries import config
from interfaces import IDispatcher

def initialize(context):
    pass
    #from mail import MailDispatcher
    #ContentInit(config.PROJECTNAME + ': dispatchers',
    #            content_types=(MailDispatcher,),
    #            ).initialize(context)

class BaseDispatcher(SimpleItem):
    implements (IDispatcher)
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    def __init__(self, id):
        self.id = id

    def dispatch(self, event):
        raise NotImplementedError('')

InitializeClass(BaseDispatcher)