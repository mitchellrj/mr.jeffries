from Products.CMFCore.utils import getToolByName, ToolInit

import config
import dispatchers
import events
import listeners
from tool import MonitorTool

def initialize(context):
    ToolInit(config.PROJECTNAME +': tools', tools=(MonitorTool,),
             product_name=config.PROJECTNAME,
             icon="resource/icon.png"
             ).initialize(context)

    dispatchers.initialize(context)
    events.initialize(context)
    listeners.initialize(context)

def reregisterHandlers():
    import Zope2
    app = Zope2.app()
    for p in app.objectValues('Plone Site'):
        tool_instance = getToolByName(p, config.TOOL_NAME, None)
        if tool_instance:
            tool_instance.initializeHandlers()

reregisterHandlers()