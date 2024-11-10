import requests
from main import register_command

def register():
    register_command('api_call')(api_call)

def api_call(args):
    """Makes an API call and returns JSON payload."""
    if not args:
        return "Usage: api_call <URL>"
    url = args[0]
    response = requests.get(url)
    return response.json()
