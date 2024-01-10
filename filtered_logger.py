#!/usr/bin/env python3
"""Defines a filter function"""
import re


def filter_datum2(fields, redaction, message, seperator):
    """Obfuscate fileds in message with redaction"""
    message = message.split(seperator)
    for field in fields:
        for m in message:
            if re.match(field, m):
                message[message.index(m)] = str(re.sub('=.*', '=' + redaction, m))
    return ';'.join(message)


def filter_datum(fields, redaction, message, seperator):
    """Obfuscate fields in message with redaction
    """
    message = message.replace(seperator, ' ')
    for field in fields:
        message = str(re.sub(field + '=\w(\w|\/)*', field + '=' + redaction, message))
    return message.replace(' ', seperator)
