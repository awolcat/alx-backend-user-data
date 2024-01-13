#!/usr/bin/env python3
"""
Main file
"""

import logging
import csv


get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

with open('user_data.csv') as csv_file:
    messages = csv.DictReader(csv_file)
    logger = get_logger()
    for message in messages:
        kv_string = ''
        row = []
        for k, v in message.items():
            kv_string = f'{k}={v}'
            row.append(kv_string)
        logger.info(';'.join(row))
