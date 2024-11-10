import mysql.connector
from command_registry import register_command

def register():
    register_command('db_query')(db_query)

def db_query(args):
    """Executes a MySQL query and returns results in Markdown."""
    if len(args) < 4:
        return "Usage: db_query <host> <user> <password> <database> <query>"
    host, user, password, database, *query = args
    query = ' '.join(query)
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host, database=database)
    cursor = cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    cnx.close()
    
    # Convert to Markdown table
    markdown = '| ' + ' | '.join(headers) + ' |\n'
    markdown += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
    for row in rows:
        markdown += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
    return markdown
import os
import psycopg2
from command_registry import register_command

def db_query(args):
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
        return f"Error: Missing required environment variables: {', '.join(missing_vars)}"

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
