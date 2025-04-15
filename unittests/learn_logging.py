import logging

logger = logging.getLogger(__name__)

def log_level_example():
    logger.debug("Debugging message")
    logger.info("Informational message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


def main():
    global logger
    logger.setLevel(logging.DEBUG)
    log_level_example()


if __name__ == '__main__':
    main()
