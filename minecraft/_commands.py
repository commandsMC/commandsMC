from .utils.events import stop_event

def stop_event_bot(bot, message):
    """
    Stop an event by name.
    """
    if not len(message.message.split()) == 2:
        bot.chat('Invalid command. Example !stop <NAME FUNCTION>')
        return
    
    if stop_event(message.message.split()[1]):
        bot.chat('Event stopped.')
    else:
        bot.chat('Event not found.')
    return