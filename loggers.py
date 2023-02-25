"""Module containing logging config for multiple loggers"""
import logging.config

import yaml


with open('logging.yaml', 'rt', encoding="utf8") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

ai_logger = logging.getLogger('ai')
board_logger = logging.getLogger('board')
