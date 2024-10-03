from typing import Dict, Any, List

def _is_exists_command(command: str, commands: List[Dict[str, Any]]) -> bool:
    """
    Check if the command exists in the list of commands.
    
    - command: str - The command to check.
    - commands: List[Dict[str, Any]] - The list of commands to check.
    """
    return any(command == c['name'] for c in commands)