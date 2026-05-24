import time
from functools import wraps

from loguru import logger


def log_stage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info(
                f"{func.__name__} ran successfully. Time elapsed: {elapsed:.3f}s"
            )
            return result
        except Exception as e:
            logger.exception(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise

    return wrapper
