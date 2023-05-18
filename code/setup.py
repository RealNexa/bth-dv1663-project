from functions import print_and_log
import functions
import logging

def initialize(session, db_name):
    """Create and use database. Create and insert "default" values into tables"""
    create_and_use_database(session, db_name)

    if create_table_parts(session):
        insert_into_parts(session)

    if create_table_prebuilt_computers(session):
        insert_into_prebuilt_computers(session)

    if create_table_prebuilt_computers_parts(session):
        insert_into_prebuilt_computers_parts(session)
    
    if create_table_customers(session):
        insert_into_customers(session)

    if create_table_orders(session):
        functions.make_order(session, "person3", 1)
        functions.make_order(session, "person4", 4)
        functions.make_order(session, "person1", 2)


    session.sql("DROP TRIGGER IF EXISTS decrementStock").execute()
    decrement_stock_trigger = \
    """ 
    CREATE TRIGGER decrementStock AFTER INSERT ON Orders FOR EACH ROW
    BEGIN
        UPDATE PrebuiltComputers SET Stock = Stock - 1 WHERE ComputerID = New.ComputerID;
    END
    """
    session.sql(decrement_stock_trigger).execute()
    print_and_log("Created trigger \"decrement_stock_trigger\"", logging.INFO)
    
    
    session.sql("DROP FUNCTION IF EXISTS usernameExist").execute()
    # create a SQL function that check if the username exists in Customers when logging in
    check_login_username_function = \
    """
    CREATE FUNCTION usernameExist(inpUsername TEXT)
    RETURNS BOOL DETERMINISTIC
    BEGIN
        DECLARE varUsernameExist INT;
        SELECT COUNT(*) FROM CUSTOMERS WHERE Username = inpUsername INTO varUsernameExist;
        IF (varUsernameExist = 1) THEN
            RETURN True;
        ELSE 
            RETURN False;
        END IF;
    
    END
    """
    session.sql(check_login_username_function).execute()
    print_and_log("Created Function \"usernameExist\"", logging.INFO)


    session.sql("DROP FUNCTION IF EXISTS validUsername").execute()
    # creates a SQL function that check if the username is valid when registering
    check_register_username_function = \
    """
    CREATE FUNCTION validUsername(inpUsername TEXT)
    RETURNS BOOL DETERMINISTIC
    BEGIN
        DECLARE duplicate INT;
        SELECT count(username) FROM Customers WHERE username = inpUsername INTO duplicate;
        
        IF (LENGTH(inpUsername) > 30 OR LENGTH(inpUsername) < 3) THEN
            RETURN False;
            
        ELSEIF (duplicate > 0) THEN
            RETURN False;
            
        ELSE
            RETURN True;

        END IF;

    END
    """
    session.sql(check_register_username_function).execute()
    print_and_log("Created Function \"validUsername\"", logging.INFO)


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
    Username VARCHAR(30) NOT NULL UNIQUE,
    Fname VARCHAR(20) NOT NULL,
    Lname VARCHAR(20) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    ShippingAddress VARCHAR(50) NOT NULL,
    InvoiceAddress VARCHAR(50) NOT NULL,

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
    ComputerID = [1, 2, 3, 4]
    PartID = [
        [1, 4, 6, 7, 9],
        [2, 4, 5, 7,10],
        [2, 3, 5, 8, 9],
        [1, 3, 5, 7, 9]
        ]
    
    for index, computer in enumerate(ComputerID):
        for part in PartID[index]:
            try:
                session.sql(f"INSERT INTO prebuiltComputersParts (ComputerID, PartID) VALUES ({computer}, {part})").execute()
                print_and_log(f"INSERT INTO prebuiltComputersParts (ComputerID, PartID) VALUES ({computer}, {part})", logging.INFO)
            except Exception as e:
                print_and_log(f"UNABLE: INSERT INTO prebuiltComputersParts (ComputerID, PartID) VALUES ({computer}, {part}), error: {e}", logging.ERROR)

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
    brand =       ["Intel",      "AMD",           "Corsair",        "G.Skill",        "MSI",              "MSI",             "ASUS",                    "MSI",               "Corsair",     "Thermaltake"]
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
