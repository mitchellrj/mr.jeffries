from zope.interface import Attribute, Interface

class IListener(Interface):

    id = Attribute('')
    event_interfaces = Attribute('')
    event_type = Attribute('')

    def notify(self, event):
        pass

    def _getHandle(self):
        pass