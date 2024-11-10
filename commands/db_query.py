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
