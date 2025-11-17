from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont

class RegisterWindow(QWidget):
    def __init__(self, users):
        super().__init__()
        self.setWindowTitle("HardTrack - Registration")
        self.resize(800, 800)
        self.setStyleSheet("background-color: #f7fafc; border-radius: 12px;")

        self.users = users

        self.username_label = QLabel("Register Username")
        self.username_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.username_label.setStyleSheet("color: #333; margin-bottom: 1px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter new username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet("padding: 9px; border-radius: 8px; border: 1px solid #cccccc; margin-bottom: 3px; background: #ffffff")

        self.password_label = QLabel("Register Password")
        self.password_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.password_label.setStyleSheet("color: #333; margin-bottom: 1px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet("padding: 9px; border-radius: 8px; border: 1px solid #cccccc; margin-bottom: 8px; background: #ffffff")

        self.register_button = QPushButton("Register")
        self.register_button.setFont(QFont("Arial", 13, QFont.Bold))
        self.register_button.setStyleSheet("background-color: #3069f1; color: white; padding: 10px; border: none; border-radius: 8px; margin-top: 7px;")
        self.register_button.clicked.connect(self.register_account)

        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(22, 0, 22, 10)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def register_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Both fields are required.")
            return
        if username in self.users:
            QMessageBox.warning(self, "Error", "Username already exists.")
        else:
            self.users[username] = {"password": password, "role": "user"}
            QMessageBox.information(self, "Success", f"User '{username}' has been registered!")
            self.close()
