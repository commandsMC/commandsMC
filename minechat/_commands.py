from .utils.events import stop_event, stop_all_events

def stop_event_bot(bot, message):
    """
    Stop an event by name.
    """
    if bot.admin and not message.user == bot.admin:
        bot.chat('You are not the admin.')
        return
    
    if not len(message.message.split()) == 2:
        bot.chat('Invalid command. Example !stop <NAME FUNCTION>')
        return
    
    if stop_event(message.message.split()[1]):
        bot.chat('Event stopped.')
    else:
        bot.chat('Event not found.')
    return

def stop_all_events_bot(bot, message):
    """
    Stop all events.
    """
    if bot.admin and not message.user == bot.admin:
        bot.chat('You are not the admin.')
        return
    
    stop_all_events()
    bot.chat('All events stopped.')
    return