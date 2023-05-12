import mysqlx
import logging
from datetime import datetime 
import setup
import functions
from enum import Enum
import GUI
from PySide6 import QtCore, QtWidgets, QtGui

# Info to connect to mysql
SQL_HOST = 'localhost'
SQL_PORT = 33060
SQL_USER = 'tomcat'
SQL_PASS = 'tomcat14'

# database info
SQL_DATABASE_NAME = 'computerStore'
    
LOG_TIME_FORMAT = r"%d-%m-%Y %H.%M.%S"


def main():
    # Creates a log file
    logging.basicConfig(
        filename=f"logging/{datetime.now().strftime(LOG_TIME_FORMAT)}.log",
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

    setup.initialize(session, SQL_DATABASE_NAME)


    app = QtWidgets.QApplication([])
    
    login_window = GUI.Login(session)
    login_window.show()

    app.exec()


if __name__ == '__main__':
    main()
