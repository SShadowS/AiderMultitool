import requests
import os
from command_registry import register_command

def get_workitem(args):
    """Fetches Azure DevOps work item data and returns a task for Aider to solve."""
    if len(args) < 2:
        return "Usage: get_workitem <organization> <taskId>"

    organization = args[0]
    task_id = args[1]

    # Construct the API URL
    url = f"https://dev.azure.com/{organization}/_apis/wit/workitems/{task_id}?api-version=7.0"

    # Retrieve the personal access token (PAT) from an environment variable
    pat = os.getenv('AZURE_DEVOPS_PAT')
    if not pat:
        return "Error: Azure DevOps Personal Access Token (PAT) not found in environment variable 'AZURE_DEVOPS_PAT'."

    # Set up authentication
    auth = ('', pat)
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Make the API request
        response = requests.get(url, auth=auth, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"HTTP Request failed: {e}"

    # Parse the response JSON
    work_item = response.json()

    # Extract necessary details to formulate a task for Aider
    title = work_item.get('fields', {}).get('System.Title', 'No Title')
    description = work_item.get('fields', {}).get('System.Description', 'No Description')

    # Create a task for Aider to solve
    task_for_aider = f"Task ID: {task_id}\nTitle: {title}\nDescription: {description}"

    return task_for_aider

def register():
    register_command('get_workitem')(get_workitem)
import os
import logging
# Configure logging
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    raise ImportError(
        "The 'requests' library is required for this command. Install it using:\n"
        "pip install -r commands/api_call_requirements.txt"
    )

from command_registry import register_command

def get_workitem(args, debug=False):
    """Fetches Azure DevOps work item data and returns the task details."""
    if not args or len(args) < 2:
        return "Usage: get_workitem <organization> <taskId>"

    organization = args[0]
    task_id = args[1]
    pat_token = os.getenv('AZURE_DEVOPS_PAT')

    if not pat_token:
        error_msg = "Error: AZURE_DEVOPS_PAT environment variable is not set."
        if debug:
            logger.error(error_msg)
        return error_msg

    try:
        # Prepare the API request
        url = f"https://dev.azure.com/{organization}/_apis/wit/workitems/{task_id}?api-version=6.0"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {pat_token}'
        }

        if debug:
            logger.debug(f"Making request to: {url}")
            
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {e}"
        if debug:
            logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        if debug:
            logger.error(error_msg)
        return error_msg

def register():
    register_command('get_workitem')(get_workitem)
