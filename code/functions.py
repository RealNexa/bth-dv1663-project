import logging
from random import randint

def print_and_log(message, level=logging.INFO):
    print(message)
    logging.log(msg=message, level=level)


def make_order(session, username, computerID):
    avail_stock = session.sql(f"SELECT stock FROM prebuiltcomputers WHERE ComputerID = {computerID}").execute().fetch_one()[0]
    if avail_stock == 0:
        return False
    random_shipping_date_offset = randint(3,10)
    try:
        session.sql(f"INSERT INTO orders (username, computerID, OrderDate, ShippingDate) VALUES ('{username}', {computerID}, NOW(), DATE_ADD(CURDATE(), INTERVAL {random_shipping_date_offset} DAY))").execute()
        print_and_log(f"INSERT INTO orders (username, computerID, OrderDate, ShippingDate) VALUES ('{username}', {computerID}, NOW(), DATE_ADD(CURDATE(), INTERVAL {random_shipping_date_offset} DAY))")
        return True
    except Exception as e:
        print_and_log(f"Unable: INSERT INTO orders (username, computerID, OrderDate, ShippingDate) VALUES ('{username}', {computerID}, NOW(), DATE_ADD(CURDATE(), INTERVAL {random_shipping_date_offset} DAY)), error: {e}", logging.ERROR)
        return False


def valid_username(session, username):
    """Uses a SQL function to check if a username is a valid username for registation"""
    print_and_log(f"SELECT validUsername('{username}')", logging.INFO)
    check_login = session.sql(f"SELECT validUsername('{username}')").execute().fetch_one()[0]
    return bool(check_login)


def username_exists(session, username):
    """Uses a SQL function to check if a username is registered"""
    print_and_log(f"SELECT validUsername('{username}')", logging.INFO)
    check_login = session.sql(f"SELECT usernameExist('{username}')").execute().fetch_one()[0]
    return bool(check_login)


def get_computers(session):
    print_and_log(f"SELECT * FROM prebuiltcomputers", logging.INFO)
    results = session.sql(f"SELECT * FROM prebuiltcomputers").execute().fetch_all()
    return results


def get_computer_info(session, id):
    print_and_log(f"SELECT * FROM prebuiltcomputers WHERE ComputerID = {id}", logging.INFO)
    results = session.sql(f"SELECT * FROM prebuiltcomputers WHERE ComputerID = {id}").execute().fetch_all()
    return results


def get_computer_parts(session, id):
    print_and_log(f"SELECT name, type, brand, releasedate, description FROM prebuiltcomputersparts AS pcp JOIN parts ON parts.PartID=pcp.PartID WHERE ComputerID = {id};", logging.INFO)
    results = session.sql(f"SELECT name, type, brand, releasedate, description FROM prebuiltcomputersparts AS pcp JOIN parts ON parts.PartID=pcp.PartID WHERE ComputerID = {id};").execute().fetch_all()
    return results


def get_user_orders(session, username):
    query = f"""
    SELECT ComputerName, CONCAT(c.Fname, " ", c.Lname) AS Name, OrderDate, ShippingDate, ShippingAddress, InvoiceAddress
    FROM Customers c JOIN Orders o ON c.Username=o.Username
    JOIN prebuiltcomputers pc ON o.ComputerID=pc.ComputerID WHERE c.Username="{username}";
    """

    print_and_log(query, logging.INFO)
    results = session.sql(query).execute().fetch_all()
    return results