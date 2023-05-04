import mysqlx
import logging
from datetime import datetime 

# Info to connect to mysql
SQL_HOST = 'localhost'
SQL_PORT = 33060
SQL_USER = 'tomcat'
SQL_PASS = 'tomcat14'

# database info
SQL_DATABASE_NAME = 'test'

LOG_TIME_FORMAT = r"%d-%m-%Y %H.%M.%S"



def main():
    
    # Creates a log file
    logging.basicConfig(
        filename=f"logs/{datetime.now().strftime(LOG_TIME_FORMAT)}.log",
        format='%(levelname)s: %(message)s',
        filemode="a",
        level=logging.INFO
    )

    logging.info("Starting program")

    # Try to connect to MySQL
    try:
        logging.info(f"Connecting to MySQL: {SQL_USER}@{SQL_HOST}:{SQL_PORT}")
        session = mysqlx.get_session({
            'host': SQL_HOST,
            'port': SQL_PORT,
            'user': SQL_USER,
            'password': SQL_PASS
        })

    except Exception as e:
        logging.error(e)
        print(f"Cannot connect to MySQL with {SQL_USER}@{SQL_HOST}:{SQL_PORT}")
        print(e)
        exit(-1)

    # Try to create database
    try:
        session.sql(f'CREATE DATABASE {SQL_DATABASE_NAME};').execute()
        logging.info(f"Creating databse \"{SQL_DATABASE_NAME}\"")
    except Exception as e:
        logging.warning(f"Database \"{SQL_DATABASE_NAME}\" already exitst")

if __name__ == '__main__':
    main()