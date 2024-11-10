import argparse
import sys
import importlib
import pkgutil
import os
import logging
from command_registry import COMMANDS, get_command

# Configure logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def load_commands(debug):
    """Dynamically load and register command modules from the 'commands' package."""
    import commands
    for loader, module_name, is_pkg in pkgutil.iter_modules(commands.__path__):
        try:
            module = importlib.import_module(f'commands.{module_name}')
            if hasattr(module, 'register'):
                module.register()
        except ImportError as e:
            if debug:
                logger.debug(f"Skipping command '{module_name}' due to missing dependencies.")
                logger.debug(str(e))
        except Exception as e:
            if debug:
                logger.error(f"Error loading {module_name}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Multi-tool command-line application.')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('command', help='Command to execute.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command.')
    
    args = parser.parse_args()
    
    # Set debug mode from args or environment
    debug = args.debug or os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    if debug:
        logger.setLevel(logging.DEBUG)

    # Load commands
    load_commands(debug)

    # Dispatch command
    command_func, help_text = get_command(args.command)
    if not command_func:
        print(f"Unknown command '{args.command}'.")
        print("\nAvailable commands:")
        for cmd_name, cmd_info in COMMANDS.items():
            print(f"\n{cmd_name}:")
            print(f"  {cmd_info['help'].strip()}")
        sys.exit(1)
    
    # Show help if no arguments provided
    if not args.args:
        print(help_text)
        sys.exit(0)
        
    # Execute command
    try:
        result = command_func(args.args, debug=debug)
        if result is not None:
            print(result)
    except ImportError as e:
        if debug:
            logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        if debug:
            logger.error(f"An error occurred while executing the command: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
