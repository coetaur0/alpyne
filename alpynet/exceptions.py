"""
Definition of exceptions.
"""

# APN exceptions.


class ConsumeException(Exception):
    """
    Exception raised when an attempt to consume a token in a place where it
    doesn't exist is made.
    """


class FiringException(Exception):
    """
    Exception raised when an attempt to fire a transition that is not fireable
    is made.
    """
