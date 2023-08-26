from loguru import logger

logger.remove(0)
logger.add(
    './cli.log',
    format='[{time:HH:MM:SS}] [{level}] {message}',
    level='DEBUG',
    rotation='100 MB',
    encoding='utf-8',
    colorize=True,
    catch=True,
)


def get_logger(name):
    """
    Get a logger with the specified name.
    """
    return logger.bind(name=name)


def trace(msg: str): logger.trace(msg)
def debug(msg: str): logger.debug(msg)
def info(msg: str): logger.info(msg)
def success(msg: str): logger.success(msg)
def warning(msg: str): logger.warning(msg)
def warn(msg: str): logger.warning(msg)
def error(msg: str): logger.error(msg)
def critical(msg: str): logger.critical(msg)
def crit(msg: str): logger.warning(msg)
def exception(msg: str): logger.exception(msg)
def catch(func_cls: callable): return logger.catch(func_cls)
