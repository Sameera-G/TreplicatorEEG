import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class ThirdPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        button = QPushButton("Go Back", self)
        button.clicked.connect(self.goBack)
        layout.addWidget(button)
        self.setLayout(layout)

    def goBack(self):
        self.hide()  # Hide the current page
        # Show the previous page (assuming it's stored as a member variable in the parent widget)
        if self.parentWidget():
            self.parentWidget().show()

class SecondPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        button = QPushButton("Go to Third Page", self)
        button.clicked.connect(self.goToThirdPage)
        layout.addWidget(button)
        self.setLayout(layout)

    def goToThirdPage(self):
        # Hide the current page
        self.hide()
        # Show the third page
        self.thirdPage = ThirdPage(parent=self)
        self.thirdPage.show()

class FirstPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        button = QPushButton("Go to Second Page", self)
        button.clicked.connect(self.goToSecondPage)
        layout.addWidget(button)
        self.setLayout(layout)

    def goToSecondPage(self):
        # Hide the current page
        self.hide()
        # Show the second page
        self.secondPage = SecondPage(parent=self)
        self.secondPage.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FirstPage()
    window.show()
    sys.exit(app.exec_())
