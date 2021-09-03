from contextlib import contextmanager

@contextmanager
def missing_dict_key_handler():
    try:
        yield 
    finally:
        return None