COMMANDS = {}

def register_command(name, help_text=None):
    """
    Decorator to register a new command.
    
    Args:
        name (str): Name of the command to register
        help_text (str, optional): Help text describing the command's usage
    """
    def decorator(func):
        COMMANDS[name] = {
            'func': func,
            'help': help_text or func.__doc__ or 'No help available.'
        }
        return func
    return decorator

def get_command(name):
    """
    Get a command function by name.
    
    Args:
        name (str): Name of the command to retrieve
        
    Returns:
        tuple: (function, help_text) if command exists, (None, None) if not
    """
    if name in COMMANDS:
        return COMMANDS[name]['func'], COMMANDS[name]['help']
    return None, None
