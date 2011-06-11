import getpass
import socket

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName
from zope.interface import implements

from mr.jeffries.dispatchers import BaseDispatcher
from interfaces import IDispatcher

class MailDispatcher(BaseDispatcher):

    implements(IDispatcher)
    title = 'mr.jeffries mail dispatcher'
    meta_type = 'Mail Dispatcher'

    default_message_format = '%(message)s'
    default_subject_format = '[%(host)s] [%(level)s] %(subject)s'

    def __init__(self, id, mail_to=None, mail_from=None, subject_format=None,
                 message_format=None):
        self.id = id
        self.mail_to = mail_to
        self.mail_from = mail_from
        self.subject_format = subject_format
        self.message_format = message_format

    def dispatch(self, event):
        mh = getToolByName(self, 'MailHost')
        portal = getToolByName(self, 'portal_url').getPortalObject()
        host = getattr(self, 'REQUEST', {}).get('HTTP_HOST', socket.getfqdn())
        data = {'host': host}
        data.update(event.data)
        data.update({'subject': event.subject, 'level': event.level,
                     'message': event.message, 'data': event.data})

        subject = (self.subject_format or self.default_subject_format) % data
        message = (self.message_format or self.default_message_format) % data

        mail_to = self.mail_to or \
                    portal.getProperty('email_from_address') or \
                   '%s@%s' % (getpass.getuser(), data['host'])

        mail_from = self.mail_from or \
                    portal.getProperty('email_from_address') or \
                   '%s@%s' % (getpass.getuser(), data['host'])

        try:
            mh.send(message, mail_to, mail_from, subject, immediate=True)
        except:
            #TODO
            pass

InitializeClass(MailDispatcher)