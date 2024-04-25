import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QEventLoop
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
import time
import subprocess
sys.path.append('I:/Research/TreplicatorEEG/utilities_files')
from stop_watch import StopWatch
from firebase_func import Firebase
from retrive_role_id import RetriveRoleId
from keep_data import KeepData

# Splash screen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

class FirestoreApp(QWidget):
    def __init__(self, selected_role, user_id, parent=None, timer=None):
        super().__init__()
        self.selected_role = selected_role
        self.user_id = user_id
        self.firebase = Firebase()
        self.parent = parent  # Reference to TaskReplicatorApp
        self.timer = QTimer(timer)  # Receive the timer instance
        self.elapsedTime = 0  # Keep track of the elapsed time
        self.initUI()
        self.startStopwatch()

    def initUI(self):
        #style  define
        style_1 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;"
        style_2 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 20px;"
        self.setWindowTitle("Task Replicator")
        self.setGeometry(100, 100, 600, 400)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background1.png")))  # Ensure you have this image
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Title space to display selected role
        self.titleLabel = QLabel(self.selected_role, self)
        self.titleLabel.setFont(QFont('Arial', 18))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: white; border-radius: 15px; padding: 20px; background-color: rgba(0, 0, 0, 150);")
        layout.addWidget(self.titleLabel)

        # Back button
        self.backButton = QPushButton('Back', self)
        self.backButton.clicked.connect(self.goBack)
        self.backButton.setFont(QFont('Arial', 12))
        self.backButton.setStyleSheet(style_1)
        layout.addWidget(self.backButton, alignment=Qt.AlignLeft)

        # User ID input
        user_id_layout = QHBoxLayout()  # Horizontal layout for user ID label and text field
        user_id_label = QLabel('User ID:', self)
        user_id_label.setFont(QFont('Arial', 12))
        user_id_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 5px;")
        user_id_layout.addWidget(user_id_label)
        
        self.user_id_entry = QLineEdit(self)
        self.user_id_entry.setFont(QFont('Arial', 12))
        self.user_id_entry.setStyleSheet("padding: 10px; border-radius: 15px;")
        user_id_layout.addWidget(self.user_id_entry)
        layout.addLayout(user_id_layout)

        #have a space
        paragraph_label3 = QLabel(f"{self.selected_role} - Pre-Defined Task", self)
        paragraph_label3.setAlignment(Qt.AlignCenter)
        paragraph_label3.setWordWrap(True)
        paragraph_label3.setFont(QFont('Arial', 12))
        paragraph_label3.setStyleSheet(style_2)
        layout.addWidget(paragraph_label3)

        # Read and display the paragraph based on the selected role
        paragraph_label2 = QLabel("Initially, a pre-defined task is carried out. Read the below paragraph and do the task", self)
        paragraph_label2.setAlignment(Qt.AlignCenter)
        paragraph_label2.setWordWrap(True)
        paragraph_label2.setFont(QFont('Arial', 12))
        paragraph_label2.setStyleSheet(style_2)
        layout.addWidget(paragraph_label2)

        # Read and display the paragraph based on the selected role
        paragraph_label = QLabel("", self)
        paragraph_label.setAlignment(Qt.AlignJustify)
        paragraph_label.setWordWrap(True)
        paragraph_label.setFont(QFont('Arial', 12))
        paragraph_label.setStyleSheet(style_2)
        layout.addWidget(paragraph_label)

        # Read paragraph from file
        paragraph_file_path = os.path.join("paragraphs", f"{self.selected_role.lower()}.txt")
        if os.path.exists(paragraph_file_path):
            with open(paragraph_file_path, "r") as file:
                paragraph_text = file.read()
            paragraph_label.setText(paragraph_text)
        else:
            paragraph_label.setText("No paragraph available for the selected role.")

        # Difficulty level input
        difficulty_layout = QHBoxLayout()  # Create QHBoxLayout for difficulty level input
        difficulty_label = QLabel('Select the difficulty level (scale from 1 to 5, 5 being hardest):', self)
        difficulty_label.setFont(QFont('Arial', 12))
        difficulty_label.setStyleSheet(style_1)
        difficulty_layout.addWidget(difficulty_label)
        
        self.difficulty_entry = QLineEdit(self)
        self.difficulty_entry.setFont(QFont('Arial', 12))
        self.difficulty_entry.setStyleSheet("padding: 10px; border-radius: 15px;")
        difficulty_layout.addWidget(self.difficulty_entry)
        layout.addLayout(difficulty_layout)

        #self.addButton = QPushButton('Add Data to Firestore', self)
        #self.addButton.clicked.connect(self.addDataToFirestore)
        #self.addButton.setFont(QFont('Arial', 12))
        #self.addButton.setStyleSheet(style_1)

        self.statusLabel = QLabel('', self)
        self.statusLabel.setFont(QFont('Arial', 12))
        self.statusLabel.setStyleSheet("color: white;")

        #layout.addWidget(self.addButton)
        layout.addWidget(self.statusLabel)
        self.setLayout(layout)

        # Next button
        self.nextButton = QPushButton('Next', self)
        self.nextButton.clicked.connect(self.goToNextPage)  # Connect to method for switching to the third page
        self.nextButton.setFont(QFont('Arial', 12))
        self.nextButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        layout.addWidget(self.nextButton, alignment=Qt.AlignRight | Qt.AlignBottom)  # Align to bottom right

        self.setLayout(layout)

        # Stopwatch display
        self.stopwatchLabel = QLabel('00:00:00', self)
        self.stopwatchLabel.setFont(QFont('Arial', 14))
        layout.addWidget(self.stopwatchLabel)

        # Connect the timer to the updateStopwatch method
        self.timer.timeout.connect(self.updateStopwatch)

    def goBack(self):
        self.hide()  # Just hide instead of closing, so it can be shown again
        if self.parent:
            self.parent.show()  # Show the TaskReplicatorApp window again

    def addUser(self):
        user_id = self.user_id_entry.text()
        if user_id:
            self.user_id_entry.setEnabled(False)
            self.statusLabel.setText(f"User '{user_id}' added.")
    
    """def addDataToFirestore(self):
        user_input = self.difficulty_entry.text()
        user_id = self.user_id_entry.text()
        if user_input and user_id:
            # Construct the Firestore path based on the selected_role and user_id
            doc_ref = db.collection(self.selected_role).document(user_id)
            doc_ref.set({'hardness_level': int(user_input)})
            self.statusLabel.setText("Difficulty level added to Firestore")
            self.difficulty_entry.clear()

            # Modify the field name to adhere to Firestore's naming conventions
            elapsed_time_key = "nuclear_physics_description_read_time"

            # Add the elapsed time to Firestore in seconds
            doc_ref.update({elapsed_time_key: self.elapsedTime})"""

        
    # Stopwatch methods
    def startStopwatch(self):
        if self.timer and not self.timer.isActive():
            self.timer.start(1000)  # Update the timer every second.

    def updateStopwatch(self):
        self.elapsedTime += 1
        elapsed_time_string = '{:02d}:{:02d}:{:02d}'.format(self.elapsedTime // 3600, (self.elapsedTime % 3600 // 60), self.elapsedTime % 60)
        self.stopwatchLabel.setText(elapsed_time_string)
    
    def store_data(self, selected_role, user_id):
        """Stores user data in a temporary file."""
        with open("user_data.tmp", "w") as file:
            data = {"selected_role": selected_role, "user_id": user_id}
            json.dump(data, file)

    @pyqtSlot()
    def goToNextPage(self):
        # Show the splash screen
        pixmap = QPixmap("images/loading.jpg")
        splash = SplashScreen(pixmap)
        splash.show()

        user_id = self.user_id_entry.text()
        keepdata = KeepData()
        keepdata.set_user_id(str(user_id))

        # Example usage (assuming you have the data)
        selected_role = self.selected_role
        
        self.store_data(selected_role, user_id)

        # Modify the field name to adhere to Firestore's naming conventions
        elapsed_time_key = "basic_description_read_time"
        self.firebase.add_data(self.selected_role, user_id, {elapsed_time_key: self.elapsedTime})

        # Define a dictionary mapping roles to corresponding actions
        actions = {
            "Teacher": lambda: subprocess.Popen(["python", "teacher_pages/thirdpage.py", self.selected_role, user_id]),
            "Software Engineer": lambda: subprocess.Popen(["python", "software_eng_pages/thirdpgsoft.py", self.selected_role, user_id]),
        }
        # Get the action corresponding to the selected_role, defaulting to None if not found
        action = actions.get(self.selected_role)
        # If an action is found, execute it
        if action:
            action()
        else:
            print("No action defined for the selected role.")

        self.close()  # Ensure the current PyQt5 window is closed.
        #self.openNextPage()

        # Delay before showing the next page (simulated loading time)
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)  # Adjust the delay as needed
        loop.exec_()

    """def openNextPage(self):
        # Define a dictionary mapping roles to corresponding actions
        actions = {
            "Teacher": lambda: subprocess.Popen(["python", "teacher_pages/thirdpage.py", str(self.selected_role), str(self.user_id)]),
            "Software Engineer": lambda: subprocess.Popen(["python", "software_eng_pages/thirdpgsoft.py", str(self.selected_role), str(self.user_id)]),
        }
        
        # Get the action corresponding to the selected_role, defaulting to None if not found
        action = actions.get(self.selected_role)
        
        # If an action is found, execute it
        if action:
            action()
        else:
            print("No action defined for the selected role.")"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = QTimer()
    ex = FirestoreApp("Tester", timer=timer)
    timer.timeout.connect(ex.updateStopwatch)
    ex.showMaximized()
    sys.exit(app.exec_())

