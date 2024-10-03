import threading
import time
from functools import wraps
from ..logger import logger

events  = {}

def _is_exists_thread(thread: str):
    for key, value in events.items():
        if value['thread'] == thread and not value['event'].is_set():
            return True
    return False

def stop_event(func: str) -> bool:
    response =  True if events.get(func) else False
    if response:
        logger.info(f'Stopping event {func}.')
        events[func]['event'].set()
    return response

def physicTick(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    if _is_exists_thread('physicTick'):
        logger.error('The physicTick function is already running.')
        return

    stop_event = threading.Event()
    events[func.__name__] = {
        'event': stop_event,
        'thread': 'physicTick'
    }

    def job():
        while not stop_event.is_set():
            wrapper()
            time.sleep(1)
    
    thread = threading.Thread(target=job, name='physicTick')
    thread.daemon = True
    thread.start()
    
    return wrapper