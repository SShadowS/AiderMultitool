# AiderMultitool
Tool for providing a context feedback to Aider

## Commands

### get_workitem

Fetches Azure DevOps work item data and returns the task details.

**Usage:**
```bash
python main.py get_workitem <organization> <taskId>
```

- `<organization>`: Your Azure DevOps organization name
- `<taskId>`: The ID of the work item to fetch

**Example:**
```bash
python main.py get_workitem myOrganization 12345
```

**Prerequisites:**

- Set the `AZURE_DEVOPS_PAT` environment variable with your Azure DevOps Personal Access Token (PAT):

  ```bash
  # For Linux/macOS
  export AZURE_DEVOPS_PAT=your_personal_access_token

  # For Windows Command Prompt
  set AZURE_DEVOPS_PAT=your_personal_access_token

  # For Windows PowerShell
  $env:AZURE_DEVOPS_PAT="your_personal_access_token"
  ```

- Install the required dependencies:

  ```bash
  pip install requests
  ```
