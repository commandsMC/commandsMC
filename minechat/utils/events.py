import threading
import time
from typing import Callable
from functools import wraps
from ..logger import logger

events = {}

def _is_exists_thread(thread: str):
    for key, value in events.items():
        if value['thread'] == thread and not value['event'].is_set():
            return True
    return False

def _create_event(func: Callable, **kwargs):
    events[func.__name__] = {
        'event': kwargs.get('event'),
        'thread': kwargs.get('thread')
    }

def _thread(func: Callable, thread: str, ttl: int):
    if not ttl > 0:
        raise ValueError('The ttl must be greater than 0.')

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    if _is_exists_thread(thread):
        logger.error(f'The {thread} function is already running.')
        return

    stop_event = threading.Event()
    _create_event(wrapper, event=stop_event, thread=thread)

    def job():
        while not stop_event.is_set():
            wrapper()
            time.sleep(ttl)
    
    thread = threading.Thread(target=job, name=thread)
    thread.daemon = True
    thread.start()
    
    return wrapper

def createEvent(thread: str, ttl: int):
    """
    Create an event.

    - thread: str - The name of the thread.
    - ttl: int - The time to live of the thread.
    """
    def decorator(func):
        return _thread(func, thread, ttl)
    return decorator

def is_event_running(func: str) -> bool:
    """
    If the event is running.
    """
    return True if events.get(func) and not events[func]['event'].is_set() else False

def stop_event(func: str) -> bool:
    """
    Off the event.
    """
    response = True if events.get(func) else False
    if response:
        events[func]['event'].set()
    return response

def stop_all_events():
    """
    Off all events.
    """
    for key, value in events.items():
        value['event'].set()

def physicTick(func):
    """
    Physic tick event.
    """
    return _thread(func, 'physicTick', 1)

def eyesOpen(ttl: int = 1):
    """
    Eyes open event.

    - ttl: int - The time to live of the thread.
    """
    def decorator(func):
        return _thread(func, 'eyesOpen', ttl)
    return decorator