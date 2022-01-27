from orator import DatabaseManager,Model
from main import PARAMS
database = PARAMS.DATABASE

config = {
    'postgresql': {
        'driver': 'postgres',
        'host': database.host,
        'database': database.db,    
        'user': database.username,
        'password': database.password,
        'prefix': ''
    }
}

conn = DatabaseManager(config)
Model.set_connection_resolver(conn)