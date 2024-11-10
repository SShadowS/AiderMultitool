from command_registry import register_command

def register():
    register_command('hello')(hello)

def hello(args, debug=False):
    """Returns a greeting message."""
    name = args[0] if args else 'World'
    return f'Hello, {name}!'
