import logging
def setup_logger():
    logger = logging.getLogger("sauce_demo_logger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:  
        fh = logging.FileHandler('/home/web-h-028/PycharmProjects/sauce_demo_automation/logs/test_log.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger