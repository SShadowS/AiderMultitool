import argparse
import sys
import importlib
import pkgutil
from command_registry import COMMANDS

def load_commands():
    """Dynamically load and register command modules from the 'commands' package."""
    import commands
    for loader, module_name, is_pkg in pkgutil.iter_modules(commands.__path__):
        try:
            module = importlib.import_module(f'commands.{module_name}')
            if hasattr(module, 'register'):
                module.register()
        except ImportError as e:
            print(f"Skipping command '{module_name}' due to missing dependencies.")
            print(e)
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
    try:
        result = command_func(args.args)
        print(result)
    except ImportError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while executing the command: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
