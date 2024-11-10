import os
try:
    import psycopg2
except ImportError:
    raise ImportError(
        "The 'psycopg2-binary' library is required for this command. Install it using:\n"
        "pip install -r commands/db_query_requirements.txt"
    )
from command_registry import register_command

def db_query(args, debug=False):
    """Executes a database query and returns the results."""
    if not args:
        return "Usage: db_query '<SQL_query>'"

    # Get database configuration from environment variables
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

    # Check if all required environment variables are set
    missing_vars = [k for k, v in db_config.items() if not v]
    if missing_vars:
        error_msg = f"Error: Missing required environment variables: {', '.join(missing_vars)}"
        if debug:
            logger.error(error_msg)
        return error_msg

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Execute the query
        cur.execute(args[0])
        
        # Fetch results
        results = cur.fetchall()
        
        # Close database connection
        cur.close()
        conn.close()

        return results

    except psycopg2.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def register():
    register_command('db_query')(db_query)
