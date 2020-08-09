"""Utility functions for ChalkDoc."""

# pylint: disable=W0612, W1202

import logging
import time

def start_logging():
    """Start logging level at INFO."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()


def timer(func):
    """Decorator to calculate and return runtime for wrapped functions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_result = func(*args, **kwargs)
        logging.info(f'{func.__name__} runtime: {time.time() - start_time}.')
        return function_result
    return wrapper
