import argparse
import sys
import importlib
from command_registry import COMMANDS

def load_commands():
    """Dynamically load command modules from the 'commands' package."""
    import commands
    print("Loading commands...")
    for module_name in ['hello', 'api_call', 'db_query']:
        try:
            print(f"Attempting to load {module_name}")
            module = importlib.import_module(f'commands.{module_name}')
            print(f"Module {module_name} loaded")
            if hasattr(module, 'register'):
                print(f"Registering {module_name}")
                module.register()
                print(f"Registered {module_name}")
        except Exception as e:
            print(f"Error loading {module_name}: {str(e)}")

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
