"""
ALL EVENTS

IATEvent
IActionRaisedExceptionEvent
IActionSucceededEvent
IActionWillBeInvokedEvent
IAfterCheckinEvent
IAfterTransitionEvent
IBeforeCheckoutEvent
IBeforeObjectAssignedEvent
IBeforeProfileImportEvent
IBeforeRenderKSSCommandsEvent
IBeforeTransitionEvent
IBeforeTraverseEvent
IBeforeUpdateEvent
ICallableOpaqueItemEvent
 * ICancelCheckoutEvent
 * ICheckinEvent
 * ICheckoutEvent
IConfigurationChangedEvent
IContainerEvent
IContainerModifiedEvent
ICredentialsUpdatedEvent
IEditBegunEvent
IEditBegunEvent
IEditCancelledEvent
IEditCancelledEvent
IEditFinishedEvent
IEditSavedEvent
IEndRequestEvent
IFieldEvent
IFieldRenderEvent
IFieldStorageEvent
IHTTPVirtualHostChangedEvent
IMailErrorEvent
IMailEvent
 * IMailSentEvent
IMutableEvent
IObjectAddedEvent
IObjectClonedEvent
IObjectCopiedEvent
IObjectCreatedEvent
IObjectEditedEvent
IObjectEvent
 * IObjectInitializedEvent
 * IObjectModifiedEvent
 * IObjectMovedEvent
 * IObjectRemovedEvent
IObjectWillBeAddedEvent
IObjectWillBeMovedEvent
IObjectWillBeRemovedEvent
 * IPASEvent
 * IPrincipalCreatedEvent
 * IPrincipalDeletedEvent
IProfileImportedEvent
IPropertiesUpdatedEvent
IPubEvent
 * IRegisterEvent
IRegistrationEvent
IRuleEvent
 * ISiteManagerCreatedEvent
ISkinChangedEvent
ITransitionEvent
IUserInitialLoginInEvent
 * IUserLoggedInEvent
 * IUserLoggedOutEvent
IVersionedFieldModifiedEvent
IWebDAVObjectEditedEvent
IWebDAVObjectInitializedEvent
IWickedContentAddedEvent
IWickedEvent
 * IWorkflowActionEvent
IWorkingCopyDeletedEvent
"""
from AccessControl import ClassSecurityInfo
try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import ContentInit
from zope.component import getGlobalSiteManager
from zope.interface import implements

from mr.jeffries import config
from mr.jeffries.events.interfaces import IEvent
from interfaces import IListener

def initialize(context):
    from errorlog import ErrorLogListener
    from mr.jeffries.dispatchers.mail import MailDispatcher
    ContentInit(config.PROJECTNAME + ': listeners & dispatchers',
                content_types=(ErrorLogListener,MailDispatcher),
                ).initialize(context)

def defaultEventHandle(event):
    # Conversion here
    new_event = IEvent(event)
    tool = getToolByName(new_event.context, config.TOOL_NAME)
    tool.notify(new_event)

class BaseListener(SimpleItem):
    implements(IListener)
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    event_interfaces = None

    def __init__(self, id):
        self.id = id
        self.__handle = None

    @classmethod
    def _getHandle(self):
        return defaultEventHandle

    def manage_afterAdd(self, item, container):
        self._addHandle(self)

    def _addHandle(self):
        gsm = getGlobalSiteManager()
        handle = self._getHandle()
        if not [h for h in gsm.registeredHandlers() if h.handler==handle and h.required==self.event_interfaces]:
            gsm.registerHandler(handle, self.event_interfaces, info=self.id)

    def notify(self, event):
        # Do filtering here
        tool = getToolByName(self, config.TOOL_NAME)
        tool.dispatch(self, event)

InitializeClass(BaseListener)