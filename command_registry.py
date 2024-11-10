COMMANDS = {}

def register_command(name):
    """Decorator to register a new command."""
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator
