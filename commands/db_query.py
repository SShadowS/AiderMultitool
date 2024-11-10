import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from command_registry import register_command

# Configure logging
logging.basicConfig(
    filename='db_query.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def db_query(args, debug=False):
    """
    Executes a database query and returns the results.
    
    Args:
        args (list): List containing the SQL query as first element
        debug (bool): Enable debug logging if True
        
    Returns:
        list: Query results as list of dictionaries
    """
    if not args:
        return "Usage: db_query '<SQL_query>'"

    try:
        load_dotenv()
        
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
            logger.error(error_msg)
            return error_msg

        # Create database URL
        db_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        
        # Create engine and execute query
        engine = create_engine(db_url)
        with engine.connect() as conn:
            logger.info(f"Executing query: {args[0]}")
            result = conn.execute(text(args[0]))
            rows = [dict(row) for row in result]
            logger.info(f"Query returned {len(rows)} results")
            return rows

    except SQLAlchemyError as e:
        error_msg = f"Database error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return error_msg

def register():
    register_command('db_query')(db_query)
