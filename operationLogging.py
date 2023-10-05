import logging
import time

#TODO: might just integrate this to bot.py if its functionality is not expanded later

def init():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        filename=f'logs/{time.strftime("%Y-%m-%d")}.log',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

def log(toLog):
    logging.info(toLog)