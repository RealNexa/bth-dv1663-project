from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets
import functions
import mysqlx

class Login(QtWidgets.QWidget):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.resize(500, 500)
        self.setWindowTitle("Login")

        self.username_line_edit = QtWidgets.QLineEdit()
        self.layout_login = QtWidgets.QFormLayout()
        self.setLayout(self.layout_login)
        self.layout_login.addRow("Username", self.username_line_edit)

        self.layout_login.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout_login.setContentsMargins(70, 11, 70, 11)

        self.label_info = QtWidgets.QLabel()
        self.label_info.setStyleSheet("Color: RED")
        self.layout_login.addRow(self.label_info)

        self.button_login = QtWidgets.QPushButton()
        self.button_login.setText("Login")
        self.button_login.clicked.connect(self.login)

        self.button_register = QtWidgets.QPushButton()
        self.button_register.setText("Register")
        self.button_register.clicked.connect(self.register)

        self.layout_login_buttons = QtWidgets.QHBoxLayout()
        self.layout_login_buttons.addWidget(self.button_login)
        self.layout_login_buttons.addWidget(self.button_register)
        self.layout_login.addRow(self.layout_login_buttons)

    @QtCore.Slot()
    def login(self):
        uname = self.username_line_edit.text().strip()
        if functions.username_exists(self.session, uname):
            self.main_window = MainWindow(self.session, uname)
            self.main_window.show()
            self.close()
        else:
            self.label_info.setText("Username is not registered")

    @QtCore.Slot()
    def register(self):
        self.register_window = RegisterWindow(self.session, self.username_line_edit.text())
        self.register_window.setModal(True)
        self.register_window.show()


class RegisterWindow(QtWidgets.QDialog):

    def __init__(self, session, username):
        super().__init__()
        
        self.session = session

        self.setWindowTitle("Register")

        self.layout = QtWidgets.QFormLayout(self)
        
        self.username_line_edit = QtWidgets.QLineEdit()
        self.username_line_edit.setText(username)
        self.username_line_edit.setMaxLength(30)
        self.layout.addRow("Username", self.username_line_edit)

        self.fname_line_edit = QtWidgets.QLineEdit()
        self.fname_line_edit.setMaxLength(20)
        self.layout.addRow("First Name", self.fname_line_edit)

        self.lname_line_edit = QtWidgets.QLineEdit()
        self.lname_line_edit.setMaxLength(20)
        self.layout.addRow("Last Name", self.lname_line_edit)
        
        self.pnumber_line_edit = QtWidgets.QLineEdit()
        self.pnumber_line_edit.setMaxLength(15)
        self.layout.addRow("Phone Number", self.pnumber_line_edit)

        self.shipping_addr_line_edit = QtWidgets.QLineEdit()
        self.shipping_addr_line_edit.setMaxLength(50)
        self.layout.addRow("Shipping Address", self.shipping_addr_line_edit)

        self.invoice_addr_line_edit = QtWidgets.QLineEdit()
        self.invoice_addr_line_edit.setMaxLength(50)
        self.layout.addRow("Invoice Address", self.invoice_addr_line_edit)

        self.info_label = QtWidgets.QLabel()
        self.info_label.setStyleSheet("Color: Red")
        self.layout.addRow(self.info_label)

        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.clicked.connect(self.register)
        self.ok_button.setText("Register")

        self.cancel_button = QtWidgets.QPushButton()
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setText("Cancel")

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addRow(self.button_layout)

    @QtCore.Slot()
    def cancel(self):
        self.close()

    @QtCore.Slot()
    def register(self):
        uname = self.username_line_edit.text().replace(" ", "")
        fname = self.fname_line_edit.text().replace(" ", "")
        lname = self.lname_line_edit.text().replace(" ", "")
        pnumber = self.pnumber_line_edit.text().replace(" ", "")
        ship_addr = self.shipping_addr_line_edit.text().strip()
        invo_addr = self.invoice_addr_line_edit.text().strip()


        info_valid = True
        if len(fname) < 2:
            info_valid = False

        elif len(lname) < 2:
            info_valid = False

        elif len(pnumber) < 7:
            info_valid = False

        elif len(ship_addr) < 5:
            info_valid = False
        
        elif len(invo_addr) < 5:
            info_valid = False
        
        if (info_valid and functions.valid_username(self.session, uname)):
            self.session.sql(f"INSERT INTO Customers VALUES ('{uname}', '{fname}', '{lname}', '{pnumber}', '{ship_addr}', '{invo_addr}')").execute()
            self.close()

        else:
            self.info_label.setText("Registration failed, please try again")


class dataListWidgetItem(QtWidgets.QListWidgetItem):

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def set_db_index(self, index):
        self.db_index = index

    def get_db_index(self):
        return self.db_index

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, session, username):
        super().__init__()
        self.session = session
        self.username = username

        self.setWindowTitle("Purchase Menu")
        self.resize(800,600)
        self.statusBar().addWidget(QtWidgets.QLabel(f"Logged in as: {username}"))

        self.logout_button = QtWidgets.QPushButton()
        self.logout_button.setText("Log Out")
        self.logout_button.clicked.connect(self.logout)
        self.statusBar().addWidget(self.logout_button)

        self.view_orders_button = QtWidgets.QPushButton()
        self.view_orders_button.setText("View orders")
        self.view_orders_button.clicked.connect(self.view_orders)
        self.statusBar().addWidget(self.view_orders_button)

        self.cen_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.cen_widget)

        self.main_hbox = QtWidgets.QHBoxLayout()
        self.cen_widget.setLayout(self.main_hbox)

        self.vbox = QtWidgets.QVBoxLayout()
        self.main_hbox.addLayout(self.vbox) # Add Vbox layout to main Hbox

        self.computer_table = QtWidgets.QListWidget()
        self.computer_table.itemClicked.connect(self.set_details)
        self.set_list_view()
        self.vbox.addWidget(self.computer_table) # Add computer table to Vbox layout

        self.info_label = QtWidgets.QLabel()
        self.vbox.addWidget(self.info_label)  # Add Info label to Vbox layout to announce successful/unsuccessful purchase

        self.purchase_button = QtWidgets.QPushButton()
        self.purchase_button.setText("Purchase")
        self.purchase_button.clicked.connect(self.purchase)
        self.vbox.addWidget(self.purchase_button) # Add purchase button to Vbox layout

        self.details_form = QtWidgets.QFormLayout()
        self.main_hbox.addLayout(self.details_form) # add detail from to main Hbox

        self.price_label = QtWidgets.QLabel()
        self.stock_label = QtWidgets.QLabel()
        self.parts_list_view = QtWidgets.QListWidget()

        self.details_form.addRow("Parts", self.parts_list_view)
        self.details_form.addRow("Price", self.price_label)
        self.details_form.addRow("Stock", self.stock_label)



    def set_list_view(self):
        self.computer_table.clear()
        computers = functions.get_computers(self.session)
        computers = list(map(lambda x: (x[0], x[1]), computers))

        for id, computer in computers:
            item = dataListWidgetItem()
            item.setText(computer)
            item.set_db_index(id)
            self.computer_table.addItem(item)

        #self.computer_table.addItems(computers)

    @QtCore.Slot()
    def purchase(self):
        list_item = self.computer_table.currentItem()
        if list_item is not None:   # if a computer is selected
            computer_id = list_item.get_db_index()
            status = functions.make_order(self.session, self.username, computer_id)
            if status:
                self.info_label.setText("Order successfull!")
                self.info_label.setStyleSheet("Color: GREEN")
            else:
                self.info_label.setText("No stock available")
                self.info_label.setStyleSheet("Color: RED")

            self.set_details(self.computer_table.currentItem())
        else:
            self.info_label.setText("Please select a computer")
            self.info_label.setStyleSheet("Color: BLUE")

    @QtCore.Slot()
    def logout(self):
        self.widget = Login(self.session) 
        self.widget.show()
        self.close()

    @QtCore.Slot()
    def view_orders(self):
        self.order_window = OrderWindow(self.session, self.username)
        self.order_window.setModal(True)
        self.order_window.show()
    
    @QtCore.Slot(dataListWidgetItem)
    def set_details(self, widget_item: dataListWidgetItem):
        pc_info = functions.get_computer_info(self.session, widget_item.db_index)[0]
        self.price_label.setText(str(pc_info[2]) + " Kr")
        self.stock_label.setText(str(pc_info[3]))

        self.parts_list_view.clear()
        parts = functions.get_computer_parts(self.session, widget_item.db_index)
        for name, type, brand, release_date, description in parts:
            self.parts_list_view.addItem(brand + " " + name)


class OrderWindow(QtWidgets.QDialog):
    def __init__(self, session, username) -> None:
        super().__init__()

        self.session = session
        self.username = username

        self.resize(700,700)
        self.setWindowTitle("Orders")

        self.orders_table_widget = QtWidgets.QTableWidget()
        self.orders_table_widget.setColumnCount(6)
        self.orders_table_widget.setHorizontalHeaderLabels(["Computer", "Name", "Order date", "Shipping date", "Shipping address", "Invoice address"])
        self.set_orders_table_widet()
        
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.orders_table_widget)


    def set_orders_table_widet(self):
        orders = functions.get_user_orders(self.session, self.username)
        self.orders_table_widget.setRowCount(len(orders))

        for i, row in enumerate(orders):

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[0]))
            self.orders_table_widget.setItem(i,0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[1]))
            self.orders_table_widget.setItem(i,1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[2]))
            self.orders_table_widget.setItem(i,2, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[3]))
            self.orders_table_widget.setItem(i,3, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[4]))
            self.orders_table_widget.setItem(i,4, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row[5]))
            self.orders_table_widget.setItem(i,5, item)
