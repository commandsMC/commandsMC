from typing import Dict, Any, Callable, Union
from colorama import Fore
from datetime import datetime
from dataclasses import dataclass
from functools import wraps
from javascript import require, On, once, off
from .logger import logger
from .functions import _is_exists_command

mineflayer = require('mineflayer')

@dataclass
class Message:
    user: str
    message: str
    date: datetime

class Mineflayer:
    def __init__(self, **config) -> None:
        """
        Mineflayer class.

        - config: Dict[str, Any] - The configuration of the bot. https://github.com/PrismarineJS/mineflayer/tree/master?tab=readme-ov-file#echo-example
        
        ```python
        Mineflayer(
        host='localhost',
        port=54992,
        username='bot',
        version='1.8.9',
        prefix='!',
        ... # Other configurations
        )
        ```
        """
        from ._commands import stop_event_bot, stop_all_events_bot

        self.prefix = config.pop('prefix', '!')
        self.admin = config.pop('admin', None)
        self.instance = mineflayer.createBot(config)
        self.instance.admin = self.admin
        self.funcs_events = None
        self.commands = [
            {
            'name': 'help',
            'description': 'Shows all commands.',
            'function': lambda bot: bot.chat('Commands: \n' + '\n'.join(
                [f'{self.prefix}{command["name"]} - {command["description"]}' for command in self.commands if command['name'] != 'help']
                ))
            },
            {
            'name': 'stop',
            'description': f'Stop a bot event. Example {self.prefix}stop <NAME FUNCTION>',
            'function': stop_event_bot
            },
            {
            'name': 'stop_all',
            'description': 'Stop all bot events.',
            'function': stop_all_events_bot
            }
        ]
        self.echo = {
            'chat': False,
            'function': None
        }
    
    @property
    def version(self) -> str:
        return self.instance.version

    def chat(self, message: str) -> None:
        """
        Sends a message to the chat.

        - message: str - The message to send.
        """
        self.instance.chat(message)

    def load_plugin(self, plugin: str) -> None:
        """
        Loads a plugin.

        - plugin: str - The plugin to load.
        """
        try:
            self.instance.loadPlugin(plugin)
        except Exception as e:
            raise e
        
    def load_events(self, func: Callable) -> None:
        """
        Load the events of the bot.

        - func: Callable - The function that contains the events.
        """
        self.funcs_events = func

    def message_handler(self, command: Union[Dict[str, str], None] = None, echo: bool = False) -> None:
        """
        Handles the message event.

        - command: Dict[str, str] - The command to handle.
        - echo: bool - In the case that the command does not argue but the echo does. You will receive all chat messages.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            if not command and echo:
                if not self.echo['chat']:
                    logger.debug('Echo enabled.')
                    self.echo = {
                        'chat': echo,
                        'function': wrapper
                    }
            else:
                if not _is_exists_command(command['name'], self.commands):
                    logger.debug(f'Command {Fore.GREEN}{self.prefix + command["name"]}{Fore.RESET} added.')
                    self.commands.append({
                        'name': command['name'].lower().replace(' ', '_'),
                        'description': command['description'] if command.get('description') else 'No description provided.',
                        'function': wrapper
                    })
                else:
                    raise KeyError(f'The command {Fore.GREEN}{self.prefix + command["name"]}{Fore.RESET} already exists.')
            return wrapper
        return decorator
    
    def add_command(self, command: Dict[str, Any], func: Callable) -> None:
        """
        Adds a new command to the bot.

        - command: Dict[str, Any] - The command to add.
        - func: Callable - The function that will be executed when the command is called.
        """
        if 'name' not in command or 'description' not in command:
            raise KeyError('You need to provide the name and description of the command.')
        
        if _is_exists_command(command['name'], self.commands):
            raise KeyError(f'The command {Fore.GREEN}{self.prefix + command["name"]}{Fore.RESET} already exists.')

        logger.debug(f'Command {Fore.GREEN}{self.prefix + command["name"]}{Fore.RESET} added.')
        self.commands.append({
            'name': command['name'].lower().replace(' ', '_'),
            'description': command['description'],
            'function': func
        })
    
    def run(self) -> None:
        """
        Executes the bot.
        """
        if self.funcs_events:
            self.funcs_events()
        
        once(self.instance, 'login')
        logger.info(f'Bot {Fore.YELLOW}{self.instance.username}{Fore.RESET} connected.')
    
        @On(self.instance, 'chat')
        def onChat(this, user, message, *rest):
            if user == self.instance.username: return
            if not message.startswith(self.prefix):
                if self.echo['chat']:
                    self.echo['function'](self.instance, Message(user, message, datetime.now()))
                return
            
            cmd = message.split()[0]
            for command in self.commands:
                if cmd not in [self.prefix + c['name'] for c in self.commands]:
                    self.instance.chat(f'Command not found. Use {self.prefix}help to see all commands.')
                    return

                if cmd == self.prefix + command['name']:                    
                    logger.info(f'Command {Fore.GREEN}{self.prefix + command["name"]}{Fore.RESET} executed by {Fore.YELLOW}{user}{Fore.RESET}.')
                    
                    if command['name'] == 'help':
                        command['function'](self.instance)
                    else:
                        command['function'](self.instance, Message(user, message, datetime.now()))
                    return