from zope.interface import Attribute, Interface

class IEvent(Interface):

    level = Attribute('Level of the event, usually one of DEBUG, INFO, WARNING, ERROR, CRITICAL')

    subject = Attribute('')

    message = Attribute('')

    data = Attribute('')

    type = Attribute('')

    context = Attribute('')

class IErrorLogEvent(Interface):
    def __init__(self, info):
        pass

    info = Attribute('')