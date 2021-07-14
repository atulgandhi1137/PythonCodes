import logging

logging.basicConfig(level = logging.DEBUG, filename = "app.log", filemode = 'w', format = '%(name)s-%(asctime)s-%(process)s-%(levelname)s-%(message)s')

logger = logging.getLogger("My logger")

def foo():
    logger.debug('Entering foo()')

    logger.info('Exiting foo()')


foo()