import sys
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Initialize Firebase
cred = credentials.Certificate('bci-research-77b3d-02a9edb61fd4.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class FirestoreApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Firestore Data Entry App')

        # Enable frameless window and semi-transparency
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 220);")

        layout = QVBoxLayout()

        self.entry = QLineEdit(self)
        self.entry.setFont(QFont('Arial', 14))
        self.entry.setPlaceholderText("Enter your data here...")

        self.addButton = QPushButton('Add Data to Firestore', self)
        self.addButton.clicked.connect(self.addDataToFirestore)

        self.statusLabel = QLabel('', self)

        layout.addWidget(self.entry)
        layout.addWidget(self.addButton)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def addDataToFirestore(self):
        user_input = self.entry.text()
        if user_input:
            doc_ref = db.collection(u'sample_data').document()
            doc_ref.set({'data': user_input})
            self.statusLabel.setText("Data added to Firestore")
            self.entry.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirestoreApp()
    ex.show()
    sys.exit(app.exec_())