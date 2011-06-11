_FILENAME = 'monitoring.xml'

def import_config(context):
    """ Import monitoring.xml
    """

    portal = context.getSite()
    logger = context.getLogger('mr.jeffries')

    body = context.readDataFile(_FILENAME)
    if body is None:
        logger.info('Nothing to import.')
        return