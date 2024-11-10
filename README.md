# AiderMultitool
Tool for providing a context feedback to Aider

## Prerequisites

- **Python Version:** Ensure you have Python 3.x installed on your system.

- **Dependencies:** Install the required Python packages using:

  ```bash
  # Install only the dependencies you need for specific commands
  pip install -r commands/api_call_requirements.txt  # For api_call command
  pip install -r commands/db_query_requirements.txt  # For db_query command
  ```

- **Environment Variables:** Set any global environment variables needed by the application.

  - Example:

    ```bash
    # For Linux/macOS
    export GLOBAL_VARIABLE=value

    # For Windows Command Prompt
    set GLOBAL_VARIABLE=value

    # For Windows PowerShell
    $env:GLOBAL_VARIABLE="value"
    ```

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

- **Azure DevOps PAT:** Set the `AZURE_DEVOPS_PAT` environment variable with your Azure DevOps Personal Access Token:

  ```bash
  # For Linux/macOS
  export AZURE_DEVOPS_PAT=your_personal_access_token

  # For Windows Command Prompt
  set AZURE_DEVOPS_PAT=your_personal_access_token

  # For Windows PowerShell
  $env:AZURE_DEVOPS_PAT="your_personal_access_token"
  ```

- **Dependencies:** Ensure the required packages are installed:

  ```bash
  pip install -r commands/get_workitem_requirements.txt
  ```

**Debugging:**

If you encounter issues or need more detailed logs, you can enable debug mode by adding the `--debug` flag:

```bash
python main.py --debug get_workitem <organization> <taskId>
```

### api_call

Makes a call to a specified API endpoint.

**Usage:**
```bash
python main.py api_call <endpoint> [parameters]
```

**Example:**
```bash
python main.py api_call https://api.example.com/data
```

**Prerequisites:**

- **Dependencies:** Install required packages using:

  ```bash
  pip install -r commands/api_call_requirements.txt
  ```

- **API Credentials:** If the API requires authentication, set the necessary environment variables:

  ```bash
  # For Linux/macOS
  export API_KEY=your_api_key

  # For Windows Command Prompt
  set API_KEY=your_api_key

  # For Windows PowerShell
  $env:API_KEY="your_api_key"
  ```

### db_query

Executes a database query and returns the results.

**Usage:**
```bash
python main.py db_query "<SQL_query>"
```

**Example:**
```bash
python main.py db_query "SELECT * FROM users;"
```

**Prerequisites:**

- **Dependencies:** Install required packages using:

  ```bash
  pip install -r commands/db_query_requirements.txt
  ```

- **Database Configuration:** Set the following environment variables:

  ```bash
  # For Linux/macOS
  export DB_HOST=your_database_host
  export DB_PORT=your_database_port
  export DB_USER=your_database_user
  export DB_PASSWORD=your_database_password
  export DB_NAME=your_database_name

  # For Windows Command Prompt
  set DB_HOST=your_database_host
  set DB_PORT=your_database_port
  set DB_USER=your_database_user
  set DB_PASSWORD=your_database_password
  set DB_NAME=your_database_name

  # For Windows PowerShell
  $env:DB_HOST="your_database_host"
  $env:DB_PORT="your_database_port"
  $env:DB_USER="your_database_user"
  $env:DB_PASSWORD="your_database_password"
  $env:DB_NAME="your_database_name"
  ```

### hello

Outputs a friendly greeting.

**Usage:**
```bash
python main.py hello
```

**Example:**
```bash
python main.py hello
```

**Prerequisites:**

- **Dependencies:** No additional dependencies required for this command.
