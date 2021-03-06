""""
Initializes and implement DBOperationsHandler by establishing a connection to the server
"""

from ClueLite.Server.database import dbOperations as dbOps 

db_ops_handler = dbOps.DBOperationsHandler()

def get_db_ops_handler():
    # if live connection does not exist, connect to dbOperations
    if db_ops_handler.status != dbOps.DB_CONNECTED:
        db_ops_handler.conn()

    return db_ops_handler
print(db_ops_handler)