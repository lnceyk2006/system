import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox,
    QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import sqlite3


def add_stat(self, layout, label, value_widget):
        lbl = QLabel(label)
        lbl.setFont(QFont("Arial", 13))
        lbl.setStyleSheet("color: black;")
        layout.addWidget(lbl)
        value_widget.setFont(QFont("Arial", 23, QFont.Bold))
        value_widget.setStyleSheet("color: black;")
        layout.addWidget(value_widget)

class TopHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 7, 15, 7)
        layout.setSpacing(20)
        items = ["Dashboard", "Inventory", "Reports", "Suppliers"]
        for name in items:
            btn = QPushButton(name)
            btn.setFont(QFont("Arial", 11, QFont.Bold))
            btn.setStyleSheet("color: #333; background: transparent; border: none;")
            layout.addWidget(btn)
        search = QLineEdit()
        search.setPlaceholderText("Search Item")
        search.setFixedWidth(170)
        layout.addWidget(search)
        layout.addStretch()
        avatar = QLabel("Admin")
        avatar.setFont(QFont("Arial", 11))
        avatar.setStyleSheet("color: #333; margin-left: 9px;")
        layout.addWidget(avatar)

class StockTable(QWidget):
    def __init__(self, add_stock_callback=None):
        super().__init__()
        self.add_stock_callback = add_stock_callback
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(13)
        self.title = QLabel("In stock")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.title)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Product Code", "Product", "Date", "Quantity"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        self.add_btn = QPushButton("Add Stock")
        self.add_btn.setFixedSize(110, 38)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: #14bcbb;
                color: white;
                border-radius: 7px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #26cfcf;
            }
        """)
        self.add_btn.clicked.connect(self.show_add_dialog)
        layout.addWidget(self.add_btn, alignment=Qt.AlignRight)

    def show_add_dialog(self):
        if self.add_stock_callback:
            self.add_stock_callback()

    def add_product_row(self, code, name, date, qty):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(code))
        self.table.setItem(row_position, 1, QTableWidgetItem(name))
        self.table.setItem(row_position, 2, QTableWidgetItem(date))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(qty)))

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Product")
        layout = QFormLayout(self)
        self.product_code = QLineEdit()
        self.product_name = QLineEdit()
        self.quantity = QLineEdit()
        layout.addRow("Product Code:", self.product_code)
        layout.addRow("Product Name:", self.product_name)
        layout.addRow("Quantity:", self.quantity)
        self.add_btn = QPushButton("Add")
        layout.addRow(self.add_btn)
        self.add_btn.clicked.connect(self.accept)

    def get_data(self):
        return (
            self.product_code.text().strip(),
            self.product_name.text().strip(),
            self.quantity.text().strip()
        )

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(1100, 660)
        self.todays_sales = 0
        self.products_sold_today = 0
        self.inventory = []

        # Database setup
        self.conn = sqlite3.connect("inventory.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS products (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL,
            date TEXT
        )""")
        self.conn.commit()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

       

        # Right panel
        right_panel = QVBoxLayout()
        right_panel.setSpacing(0)
        right_panel.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header = TopHeader()
        right_panel.addWidget(self.header)

        # Stock Table
        self.stocktable = StockTable(self.show_add_product_dialog)
        right_panel.addWidget(self.stocktable)

        main_layout.addLayout(right_panel)

        # Load initial products from database
        self.load_products()

    def load_products(self):
        self.c.execute("SELECT code, name, stock, date FROM products")
        for code, name, stock, date in self.c.fetchall():
            self.inventory.append({'code': code, 'name': name, 'stock': stock, 'date': date})
            self.stocktable.add_product_row(code, name, date, stock)

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec_():
            code, name, qty_text = dialog.get_data()
            if code and name and qty_text:
                try:
                    qty = int(qty_text)
                    date = datetime.now().strftime("%m-%d-%Y")
                    self.add_stock_item(code, name, qty, date)
                    QMessageBox.information(self, "Added", f"Product added: {name} x{qty}")
                except Exception as e:
                    QMessageBox.warning(self, "Error", "Quantity must be a number!")

    def add_stock_item(self, code, name, qty, date):
        # Check if product exists
        self.c.execute("SELECT stock FROM products WHERE code = ?", (code,))
        result = self.c.fetchone()
        if result:
            new_qty = result[0] + qty
            self.c.execute("UPDATE products SET stock = ?, date = ? WHERE code = ?", (new_qty, date, code))
        else:
            self.c.execute("INSERT INTO products (code, name, stock, date) VALUES (?, ?, ?, ?)",
                           (code, name, qty, date))
        self.conn.commit()
        self.stocktable.add_product_row(code, name, date, qty)
        # Optionally update sidebar overview stats
        self.sidebar.orders_today.setText(str(int(self.sidebar.orders_today.text()) + 1))
        self.update_dashboard_cards()

    def update_dashboard_cards(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
