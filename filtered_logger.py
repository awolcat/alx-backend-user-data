#!/usr/bin/env python3
"""Defines a filter function"""
import re
import logging
from datetime import datetime


def filter_datum(fields, redaction, message, seperator):
    """Obfuscate fields in message with redaction
    """
    message = message.replace(seperator, ' ')
    for field in fields:
        message = str(re.sub(field + '=\w(\w|\/|@|\.|\-)*', field + '=' + redaction, message))
    return message.replace(' ', seperator)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        RedactingFormatter.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        string = filter_datum(self.FIELDS, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return str(self.FORMAT % {'name': record.name, 'levelname': record.levelname, 'asctime': datetime.utcnow(), 'message': string})
