from zope.interface import Interface, Attribute

class IDispatcher(Interface):

    def __init__(self, name):
        pass

    def dispatch(self, event):
        pass