import logging
from colorama import Fore

logger = logging.getLogger(__name__)


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger('arbiter')

    def debug(self, msg):
        self.logger.debug('%s%s%s' % (Fore.RED, msg, Fore.RESET))

    def info(self, msg):
        self.logger.info('%s%s%s' % (Fore.GREEN, msg, Fore.RESET))

    def error(self, msg):
        self.logger.error('%s%s%s' % (Fore.RED, msg, Fore.RESET))
