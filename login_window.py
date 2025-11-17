from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QLabel, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
import sys
from registration import RegisterWindow    # If you use a separate registration window
from admin_dashboard import MainWindow     # Import your dashboard

# Example users dictionary
users = {
    "admin1": {"password": "admin123", "role": "admin"},
    "cashier1": {"password": "cashier123", "role": "cashier"}
}

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HardTrack")
        self.resize(500, 500)  # Practical window size

        self.setStyleSheet("background-color: #f7fafc; border-radius: 12px;")

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("logo.png"))

        self.title_label = QLabel("HardTrack")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #3069f1; margin-top: 8px; margin-bottom: 6px;")

        self.subtitle_label = QLabel("Enter your details")
        self.subtitle_label.setFont(QFont("Arial", 10))
        self.subtitle_label.setStyleSheet("color: #444; margin-bottom: 10px;")

        self.username_label = QLabel("Username")
        self.username_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.username_label.setStyleSheet("color: #333; margin-bottom: 1px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet(
            "padding: 9px; border-radius: 8px; border: 1px solid #cccccc; margin-bottom: 3px; background: #ffffff"
        )

        self.password_label = QLabel("Password")
        self.password_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.password_label.setStyleSheet("color: #333; margin-bottom: 1px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet(
            "padding: 9px; border-radius: 8px; border: 1px solid #cccccc; margin-bottom: 8px; background: #ffffff"
        )

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setFont(QFont("Arial", 13, QFont.Bold))
        self.login_button.setStyleSheet(
            "background-color: #3069f1; color: white; padding: 10px; border: none; border-radius: 8px; margin-top: 7px;"
        )

        self.registration_button = QPushButton("Register new user")
        self.registration_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.registration_button.setStyleSheet(
            "color: #3069f1; background: transparent; border: none; margin-top: 20px;"
        )
        self.registration_button.clicked.connect(self.open_registration)

        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(22, 0, 22, 10)
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.registration_button)
        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username in users and users[username]["password"] == password:
            if users[username]["role"] == "admin":
                QMessageBox.information(self, "Login Successfully", f"Welcome, {username} (Admin)")
                self.dashboard_win = MainWindow()  # This loads the dashboard from admin_dashboard.py
                self.dashboard_win.show()
                self.close()
            else:
                QMessageBox.information(self, "Login Successfully", f"Welcome, {username} (Cashier)")
                # You could show a different dashboard for cashiers here if desired
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Credentials")
            self.password_input.clear()
            self.password_input.setFocus()

    def open_registration(self):
        self.register_win = RegisterWindow(users)
        self.register_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
