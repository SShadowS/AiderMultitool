import argparse
import sys
import importlib
import pkgutil

# Command registry
COMMANDS = {}

def register_command(name):
    """Decorator to register a new command."""
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator

def load_commands():
    """Dynamically load command modules from the 'commands' package."""
    package = 'commands'
    for loader, module_name, is_pkg in pkgutil.iter_modules([package.replace('.', '/')]):
        module = importlib.import_module(f'{package}.{module_name}')
        if hasattr(module, 'register'):
            module.register()

def main():
    parser = argparse.ArgumentParser(description='Multi-tool command-line application.')
    parser.add_argument('command', help='Command to execute.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command.')
    
    args = parser.parse_args()

    # Load commands
    load_commands()

    # Dispatch command
    command_func = COMMANDS.get(args.command)
    if not command_func:
        print(f"Unknown command '{args.command}'. Available commands: {', '.join(COMMANDS.keys())}")
        sys.exit(1)
    
    # Execute command
    result = command_func(args.args)
    print(result)

if __name__ == '__main__':
    main()
