try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass

from mr.jeffries.listeners import BaseListener
from mr.jeffries.events.interfaces import IErrorLogEvent


class ErrorLogListener(BaseListener):
    title = 'mr.jeffries error log listener'
    meta_type = 'Error Log Listener'
    event_type = 'error_log'
    event_interfaces = (IErrorLogEvent,)

InitializeClass(ErrorLogListener)