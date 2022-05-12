import psycopg2
from config import params

config = psycopg2.connect(**params)
current = config.cursor()

create_table = '''
    CREATE TABLE records(
        name VARCHAR(255) NOT NULL,
        record INT NOT NULL
    );
'''

current.execute(create_table)

current.close()
config.commit()
config.close()