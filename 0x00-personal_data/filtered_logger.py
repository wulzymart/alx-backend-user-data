#!/usr/bin/env python3
"""filter data"""

from typing import List
import re
import logging
from os import environ
import mysql.connector


# # PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """use a regex to replace occurrences of certain field values."""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """setup a new logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connection.MySQLConnection(user=username,
                                                    password=password,
                                                    host=host,
                                                    database=db_name)
    return db


def main():
    """retrives user data"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [columns[0] for columns in cursor.description]
    logger = get_logger()
    for row in cursor:
        message = ''.join(f'{field}={str(entry)}; ' for entry,
                          field in zip(row, fields))
        logger.info(message.strip())
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for filtering PII fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """new instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats the log records"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)


if __name__ == '__main__':
    main()
