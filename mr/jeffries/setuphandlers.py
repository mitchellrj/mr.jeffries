from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

import config
from tool import MonitorTool

def _migrate_tool(portal, toolid, name, attrs):
    orig = getToolByName(portal, toolid)
    portal.manage_delObjects(toolid)
    portal.manage_addProduct[config.PROJECTNAME].manage_addTool(name)
    tool = getToolByName(portal, toolid)
    for attr in attrs:
        setattr(tool, attr, aq_base(getattr(aq_base(orig), attr)))
    return aq_base(orig)

def setup_monitoring_tool(context):
    '''Replacing tool'''
    site = context.getSite()
    portal = getToolByName(site, 'portal_url').getPortalObject()
    if getToolByName(site, config.TOOL_NAME, None) is not None:
        _migrate_tool(site, config.TOOL_NAME,
                MonitorTool.meta_type,
                [])
    else:
        portal.manage_addProduct[config.PROJECTNAME].manage_addTool(MonitorTool.meta_type, None)
