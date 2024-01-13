#!/usr/bin/env python3
"""Defines a filter function"""
import re
import logging
import os
import mysql.connector
from typing import List
from datetime import datetime


PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, 
                 seperator:str) -> str:
    """Obfuscate fields in message with redaction
    """
    message = message.replace(seperator, ' ')
    for field in fields:
        message = str(re.sub(field + '=(\w|\()(\w|\/|@|\.|\-|\(|\)|)*', field + '=' + redaction, message))
    return message.replace(' ', seperator)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        RedactingFormatter.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        string = filter_datum(self.FIELDS, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return str(self.FORMAT % {'name': record.name,
                                  'levelname': record.levelname,
                                  'asctime': datetime.utcnow(),
                                  'message': string})


def get_logger() -> logging.Logger:
    """Create a logger
    """
    logger = logging.getLogger('user_data') # Get logger object
    logger.propagate = False # propagate is true by default, set false
    logger.setLevel(logging.INFO) # set logger level
    stream_handler = logging.StreamHandler() # create stream handler object 
    formatter = RedactingFormatter(fields=PII_FIELDS) # create formatter instance
    stream_handler.setFormatter(formatter) # set handler's formatter
    logger.addHandler(stream_handler) # set logger handler(s)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get db credentials from environment
        and return mysql db connection object
        for said db credentials
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME', '')

    return mysql.connector.connect(username=username,
                                   password=password,
                                   host=host,
                                   database=database)


def main():
    """Default module fuction
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users;')
    for row in cursor:
        attr_list = []
        attr_str = ''
        for k,v in row.items():
            attr_str = f'{k}={v}'
            attr_list.append(attr_str)
        filter_input = RedactingFormatter.SEPARATOR.join(attr_list)
        logger.info(filter_input)


if __name__ == '__main__':
    main()
