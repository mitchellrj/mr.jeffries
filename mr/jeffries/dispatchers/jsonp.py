import datetime

from AccessControl import ClassSecurityInfo
try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from OFS.Traversable import Traversable
import simplejson
from zope.interface import implements

from mr.jeffries.dispatchers import BaseDispatcher
from interfaces import IDispatcher

class JSONPDispatcher(BaseDispatcher, Traversable):
    security = ClassSecurityInfo()

    implements(IDispatcher)
    title = 'mr.jeffries jsonp dispatcher'
    meta_type = 'JSONP Dispatcher'

    def __init__(self, id, timeout=600):
        self.id = id
        self.timeout = timeout
        self._event_queue = []
        self._current_sessions = {}

    def _expire_sessions(self):
        to_remove = []
        for sid, lastTime in self._current_sessions.items():
            if lastTime + datetime.timedelta(seconds=self.timeout) < datetime.datetime.now():
                to_remove.append(sid)
        for sid in to_remove:
            del self._current_sessions[sid]

        if not self._current_sessions:
            self._event_queue = []

    def _expire_events(self):
        oldest = min(self._current_sessions.values())
        self._event_queue = self._events_since(oldest)

    def _events_since(self, dt):
        i = 0
        for _, t in self._event_queue:
            if t > dt:
                break
            i += 1

        return self._event_queue[i:]

    def dispatch(self, event):
        self._expire_sessions()
        if self._current_sessions:
            self._event_queue.append((event, datetime.datetime.now()))

    #def _get_session(self, REQUEST):
    #    cookies = REQUEST.response.cookies
    #        REQUEST.response.setCookie(config.COOKIE_NAME, '')

    #    if not cookies.has_key(config.COOKIE_NAME):
    #    cookie = REQUEST.response.cookies[config.COOKIE_NAME]

    #    scookie.split(',')

    security.declareProtected('Manage Portal', 'get')
    def get(self, jsonp=None):
        """ return json or jsonp
        """
        sid = self.REQUEST.SESSION.id
        since = self._current_sessions.get(sid, datetime.datetime.now())
        self._current_sessions[sid] = datetime.datetime.now()

        if jsonp:
            self.REQUEST.response.setHeader('Content-type', 'text/javascript')
        else:
            self.REQUEST.response.setHeader('Content-type', 'application/json')

        events = self._events_since(since)

        self._expire_events()

        result = json = simplejson.dumps([{'level': e.level,
                                           'type': e.type,
                                           'subject': e.subject,
                                           'message': e.message,
                                           'data': e.data} for e, _ in events])

        if jsonp:
            result = '%s(%s);' % (jsonp, json)

        return result


InitializeClass(JSONPDispatcher)