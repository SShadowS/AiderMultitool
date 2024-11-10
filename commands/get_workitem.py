import os
import logging
import base64
import requests
from bs4 import BeautifulSoup
from command_registry import register_command

# Configure logging
logger = logging.getLogger(__name__)

# Check required dependencies
if not hasattr(requests, 'get'):
    raise ImportError(
        "The 'requests' library is required for this command. Install it using:\n"
        "pip install -r commands/get_workitem_requirements.txt"
    )

if not hasattr(BeautifulSoup, '__call__'):
    raise ImportError(
        "The 'beautifulsoup4' library is required for this command. Install it using:\n"
        "pip install -r commands/get_workitem_requirements.txt"
    )

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
        # Encode the credentials
        credentials = base64.b64encode((':' + pat_token).encode('utf-8')).decode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}'
        }

        if debug:
            logger.debug(f"Making request to: {url}")
            
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        fields = data.get('fields', {})

        # Extract relevant fields
        title = fields.get('System.Title', 'No Title')
        description = fields.get('System.Description', 'No Description')
        assigned_to = fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')

        # Clean HTML tags from the description
        clean_description = BeautifulSoup(description, 'html.parser').get_text()

        # Construct the prompt
        prompt = (
            f"Implement the following task:\n"
            f"Task Title: {title}\n"
            f"Description: {clean_description}\n"
            #f"Assigned To: {assigned_to}\n"
        )

        return prompt

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
    help_text = """
    Fetches work item details from Azure DevOps.
    
    Usage: get_workitem <organization> <taskId>
    
    Arguments:
        organization: Azure DevOps organization name
        taskId: ID of the work item to fetch
        
    Environment Variables:
        AZURE_DEVOPS_PAT: Personal Access Token for Azure DevOps
    """
    register_command('get_workitem', help_text)(get_workitem)
