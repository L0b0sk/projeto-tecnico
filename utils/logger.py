import logging
import sys

def get_logger(namer:str) -> logging.logger:
    logger = logging.getLogger (namer)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    handler = logging.StemHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    
    handler.setFormatter(formatter)
    logger.addHadler(handler)
    return logger