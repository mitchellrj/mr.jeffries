from AccessControl.SecurityManagement import getSecurityManager
from zExceptions.ExceptionFormatter import format_exception
from zope.component import adapts
from zope.event import notify
from zope.interface import implements

from mr.jeffries.events import BaseEventAdapter
from interfaces import IErrorLogEvent, IEvent

class ErrorLogEvent(object):

    implements(IErrorLogEvent)

    def __init__(self, context, info):
        self.info = info
        self.context = context

class ErrorLogEventAdapter(BaseEventAdapter):
    implements(IEvent)
    adapts(IErrorLogEvent)

    type = 'error_log'

    def __init__(self, event):
        info = event.info
        tb_text = None
        tb_html = None

        strtype = str(getattr(info[0], '__name__', info[0]))

        if not isinstance(info[2], basestring):
            tb_text = ''.join(
                format_exception(*info, **{'as_html': 0}))
            tb_html = ''.join(
                format_exception(*info, **{'as_html': 1}))
        else:
            tb_text = info[2]

        request = getattr(self, 'REQUEST', None)
        url = None
        username = None
        userid   = None
        req_html = None
        try:
            strv = str(info[1])
        except:
            strv = '<unprintable %s object>' % type(info[1]).__name__
        if request:
            url = request.get('URL', '?')
            usr = getSecurityManager().getUser()
            username = usr.getUserName()
            userid = usr.getId()
            try:
                req_html = str(request)
            except:
                pass
            if strtype == 'NotFound':
                strv = url
                next = request['TraversalRequestNameStack']
                if next:
                    next = list(next)
                    next.reverse()
                    strv = '%s [ /%s ]' % (strv, '/'.join(next))

        self.context = event.context
        self.level = 'ERROR'
        self.subject = ': '.join([strtype, strv])
        self.message = tb_text
        self.data = {
            'type': strtype,
            'value': strv,
            'tb_text': tb_text,
            'tb_html': tb_html,
            'username': username,
            'userid': userid,
            'url': url,
            'req_html': req_html,
            }

# see configure.zcml for monkey patching of SiteErrorLog
def monitorRaising(self, info):
    #monitorRaising.__doc__ = self._old_raising.__doc__ + '\n\n' +\
    #                         'This has been monkey-patched by ' +\
    #                         'mr.jeffries to fire an event before ' +\
    #                         'logging the error.'
    notify(ErrorLogEvent(self, info))
    return self._old_raising(info)