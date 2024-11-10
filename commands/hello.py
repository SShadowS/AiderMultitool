from main import register_command

def register():
    print("Hello module register() called")
    register_command('hello')(hello)
    print("Hello command registered")

def hello(args):
    """Returns a greeting message."""
    name = args[0] if args else 'World'
    return f'Hello, {name}!'
