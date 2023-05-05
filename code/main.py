import mysqlx
import logging
from datetime import datetime 

# Info to connect to mysql
SQL_HOST = 'localhost'
SQL_PORT = 33060
SQL_USER = 'tomcat'
SQL_PASS = 'tomcat14'

# database info
SQL_DATABASE_NAME = 'computerStore'
    
LOG_TIME_FORMAT = r"%d-%m-%Y %H.%M.%S"

def print_and_log(message, level=logging.INFO):
    print(message)
    logging.log(msg=message, level=level)


def create_and_use_database(session, name):
    """Try to create and use database"""
    try:
        session.sql(f'CREATE DATABASE {name};').execute()
        print_and_log(f"Created database \"{name}\"", logging.INFO)
    except Exception as e:
        print_and_log(f"Unable to create database \"{name}\", error {e}", logging.WARNING)

    finally:
        session.sql(f'USE {name};').execute()
        print_and_log(f"Using database \"{name}\"", logging.INFO)



def create_table_customers(session):
    create_customers = """CREATE TABLE customers(
    Username VARCHAR(20) NOT NULL UNIQUE,
    Fname VARCHAR(20) NOT NULL,
    Lname VARCHAR(20) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    ShippingAddress VARCHAR(80) NOT NULL,
    InvoiceAddress VARCHAR(80) NOT NULL,

    PRIMARY KEY(Username)
    )
    """
    try:
        session.sql(create_customers).execute()
        print_and_log("Created table \"customers\"", logging.INFO)
        return True
    except Exception as e:
        print_and_log(f"Failed to create table \"customers\", error: {e}", logging.ERROR)
        return False

def insert_into_customers(session):
    username = ["person1", "person2", "person3", "person4", "person5"]
    first_name = ["john", "jane", "ulf", "tim", "max"]
    last_name = ["doe", "doe", "olsen", "persson", "eriksson"]
    phone_number = ["0761382743", "0438428812", "0713501134", "0123456789", "98765432190"]
    ship_addr = ["addressgatan 1", "gatan 2", "storgatan 500", "industrigatan 12", "addressen 73"]
    invoice_addr = ["addressgatan 1", "gatan 2", "enaddress 3", "julgatan 67", "stockholmsgatan 42"]

    for (uname, fname, lname, pnum, shpaddr, invoaddr) in zip(username, first_name, last_name, phone_number, ship_addr, invoice_addr):
        try:
            session.sql(f"INSERT INTO customers VALUES ('{uname}', '{fname}', '{lname}', '{pnum}', '{shpaddr}', '{invoaddr}')").execute()
            print_and_log(f"INSERT INTO customers VALUES ('{uname}', '{fname}', '{lname}', '{pnum}', '{shpaddr}', '{invoaddr}')")
        except Exception as e:
            print_and_log(f"Unable: INSERT INTO customers VALUES ('{uname}', '{fname}', '{lname}', '{pnum}', '{shpaddr}', '{invoaddr}'), error: {e}", logging.ERROR)


def create_table_orders(session):
    create_orders = """ CREATE TABLE orders (
    OrderID INT NOT NULL AUTO_INCREMENT UNIQUE,
    Username VARCHAR(20) NOT NULL,
    ComputerID INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    ShippingDate DATE NOT NULL,

    PRIMARY KEY (OrderID),
    FOREIGN KEY (Username) REFERENCES customers (Username),
    FOREIGN KEY (ComputerID) REFERENCES prebuiltComputers (ComputerID)
    )
    """

    try:
        session.sql(create_orders).execute()
        print_and_log("Created table \"Orders\"", logging.INFO)
        return True
    except Exception as e:
        print_and_log(f"Failed to create table \"Orders\", error: {e}", level=logging.ERROR)
        return False

# def insert_into_orders(session):
#     Username = ["person1", "person2", "person3", "person4"]
#     ComputerID = ["1004", "1001", "1002", "1001"]
#     OrderDate = ["2022-12-15", "2023-02-15", "2023-02-25", "2023-04-25"]
#     ShippingDate = ["2023-01-01", "2023-02-25", "2023-03-03", "2023-05-05"]

#     for (username, computerID, shippingDate, orderDate) in zip(Username, ComputerID, ShippingDate, OrderDate):
#         session.sql(f"INSERT INTO orders (Username, ComputerID, OrderDate, ShippingDate) VALUES ('{username}', '{computerID}', '{shippingDate}', '{orderDate}')").execute()



def create_table_prebuilt_computers(session):
    create_prebuilt_computers = """ CREATE TABLE prebuiltComputers (
    ComputerID INT NOT NULL AUTO_INCREMENT,
    ComputerName VARCHAR(30),
    Price INT NOT NULL,
    Stock INT,
    PRIMARY KEY(ComputerID)
    )
    """
    try:
        session.sql(create_prebuilt_computers).execute()
        print_and_log("Created table \"prebuiltComputers\"", logging.INFO)
        return True
    except Exception as e:
        print_and_log(f"Failed to create table \"prebuiltComputers\", error {e}", logging.ERROR)
        return False

def insert_into_prebuilt_computers(session):
    ComputerName = ["Karlskrona Special", "Next Gen Gaming Computer", "Traditional Work Computer", "Low-end Budget Computer"]
    Price = [64000, 33000, 15000, 10000]
    Stock = [2, 5, 100, 50]

    for (computerName, price, stock) in zip(ComputerName, Price, Stock):
        try:
            session.sql(f"INSERT INTO prebuiltComputers (ComputerName, Price, Stock) VALUES ('{computerName}', {price}, {stock})").execute()
            print_and_log(f"INSERT INTO prebuiltComputers (ComputerName, Price, Stock) VALUES ('{computerName}', {price}, {stock})")
        except Exception as e:
            print_and_log(f"Unable: INSERT INTO prebuiltComputers (ComputerName, Price, Stock) VALUES ('{computerName}', {price}, {stock}), error: {e}", logging.ERROR)



def create_table_prebuilt_computers_parts(session):
    create_prebuilt_computers_part = """ 
    CREATE TABLE prebuiltComputersParts (
    
    PCPID INT NOT NULL AUTO_INCREMENT UNIQUE,
    ComputerID INT NOT NULL,
    PartID INT NOT NULL,

    PRIMARY KEY (PCPID),
    FOREIGN KEY (ComputerID) REFERENCES prebuiltComputers (ComputerID),
    FOREIGN KEY (PartID) REFERENCES Parts (PartID)
    
    )
    """

    try:
        session.sql(create_prebuilt_computers_part).execute()
        print_and_log("Created table \"prebuiltComputersParts\"", logging.INFO)
        return True
    except Exception as e:
        print_and_log(f"Failed to create table \"prebuiltComputersParts\", error: {e}", level=logging.ERROR)
        return False

def insert_into_prebuilt_computers_parts(session):
    #TODO FIX
    pass


def create_table_parts(session):
    create_orders = """
    CREATE TABLE Parts (
    
    PartID INT NOT NULL AUTO_INCREMENT UNIQUE,
    Name VARCHAR(20) NOT NULL,
    Type VARCHAR(20) NOT NULL,
    Brand VARCHAR(20) NOT NULL,
    ReleaseDate DATE NOT NULL,
    Description TEXT,

    PRIMARY KEY (PartID)
    )
    """

    try:
        session.sql(create_orders).execute()
        print_and_log("Created table \"Parts\"", logging.INFO)
        return True
    except Exception as e:
        print_and_log(f"Failed to create table \"Parts\", error: {e}", level=logging.ERROR)
        return False

def insert_into_parts(session):
    name =        ["i9-13900K",  "Ryzen 5 5600X", "Vengeance LPX",  "Trident Z5 RGB", "GeForce RTX 3060", "RX 6600 XT MECH", "TUF GAMING X570-PLUS",    "A520M-A PRO",       "RM850x",      "Smart BM2"]
    type =        ["CPU",        "CPU",           "RAM",            "RAM",            "GPU",              "GPU",             "Motherboard",             "Motherboard",       "PSU",         "PSU"]
    brand =       ["Intel",      "AMD",           "Corsair",        "G.Skill",        "MSI",              "MSI",             "ASUS",                    "MSI"                "Corsair",     "Thermaltake"]
    releaseDate = ["2022-11-23", "2021-03-05",    "2021-04-12",     "2023-02-21",     "2021-07-11",       "2021-09-17",      "2023-01-04",              "2020-05-03",        "2021-05-02",  "2019-04-29"]
    description = [
        "3 GHz 24-Core Processor",
        "3.7 GHz 6-Core Processor",
        "LPX 16 GB (2 x 8 GB) DDR4-3200 CL16",
        "64 GB (2 x 32 GB) DDR5-6400 CL32", 
        "GeForce RTX 3060 12GB 12 GB Video Card",
        "RX 6600 XT MECH",
        "(WI-FI) ATX AM4 Motherboard",
        "MSI Micro ATX AM4",
        "850 W 80+ Gold Certified Fully Modular ATX",
        "650 W 80+ Bronze Certified Semi-modular ATX"
        ]
    
    for (Name, Type, Brand, ReleaseDate, Description) in zip(name, type, brand, releaseDate, description):
        try:
            session.sql(f"INSERT INTO parts (name, type, brand, releaseDate, description) VALUES ('{Name}', '{Type}', '{Brand}', '{ReleaseDate}', '{Description}')").execute()
            print_and_log(f"INSERT INTO parts (name, type, brand, releaseDate, description) VALUES ('{Name}', '{Type}', '{Brand}', '{ReleaseDate}', '{Description}')")
        except Exception as e:
            print_and_log(f"Unable: INSERT INTO parts (name, type, brand, releaseDate, description) VALUES ('{Name}', '{Type}', '{Brand}', '{ReleaseDate}', '{Description}'), error: {e}", logging.ERROR)


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


    create_and_use_database(session, SQL_DATABASE_NAME)

    if create_table_parts(session):
        insert_into_parts(session)

    if create_table_prebuilt_computers(session):
        insert_into_prebuilt_computers(session)

    if create_table_prebuilt_computers_parts(session):
        pass
    
    if create_table_customers(session):
        insert_into_customers(session)

    if create_table_orders(session):
        pass


if __name__ == '__main__':
    main()