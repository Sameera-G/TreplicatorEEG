import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
import pyttsx3
from PyQt5.QtCore import QTimer

from treplicator import FirestoreApp  # Import the pyttsx3 library for text-to-speech functionality.

class TaskReplicatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speech_engine = pyttsx3.init()  # Initialize the speech synthesis engine.
        self.timer = QTimer(self)  # Instantiate QTimer
        self.timer.timeout.connect(self.updateStopwatch)
        self.elapsedTime = 0  # Keep track of the elapsed time
        self.startStopwatch()

    def initUI(self):
        #title
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Task Replicator')
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background1.png")))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()

        #stop watch
        self.stopwatchLabel = QLabel('00:00:00', self)
        self.stopwatchLabel.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.stopwatchLabel)

        self.startStopButton = QPushButton('Start', self)
        self.startStopButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        self.startStopButton.clicked.connect(self.startStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)  # Convert to integer
        button_height = int(self.startStopButton.sizeHint().height())  # Convert to integer
        self.startStopButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.startStopButton)

        self.resetButton = QPushButton('Reset', self)
        self.resetButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        self.resetButton.clicked.connect(self.resetStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)  # Convert to integer
        button_height = int(self.resetButton.sizeHint().height())  # Convert to integer
        self.resetButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.resetButton)

        self.mainLabel = QLabel('Task Replicator', self)
        self.mainLabel.setFont(QFont('Arial', 18))
        self.mainLabel.setAlignment(Qt.AlignCenter)
        self.mainLabel.setStyleSheet("border-radius: 15px;")
        left_layout.addWidget(self.mainLabel)

        self.descriptionLabel1 = QLabel(self)
        self.descriptionLabel1.setFont(QFont('Arial', 12))
        self.descriptionLabel1.setAlignment(Qt.AlignCenter)
        self.descriptionLabel1.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 15px; padding: 20px; text-align: justify;")
        left_layout.addWidget(self.descriptionLabel1)

        # Listen button for the description, updated size and color as per request.
        self.listenButton = QPushButton("Listen", self)
        self.listenButton.clicked.connect(self.speakDescription)
        self.listenButton.setFont(QFont('Arial', 12))
        self.listenButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)  # Convert to integer
        button_height = int(self.listenButton.sizeHint().height())  # Convert to integer
        self.listenButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.listenButton)

        self.descriptionLabel = QLabel('Please select your desired role to proceed', self)
        self.descriptionLabel.setFont(QFont('Arial', 12))
        self.descriptionLabel.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 15px; padding: 20px; text-align: justify;")
        left_layout.addWidget(self.descriptionLabel)

        layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.buttons = []
        roles = ["Teacher", "Software Engineer", "Civil Engineer", "Doctor", "Nurse", "Labor"]
        for role in roles:
            button = QPushButton(role, self)
            button.setFont(QFont('Arial', 16))
            button.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 20px;")
            button.clicked.connect(lambda checked, r=role: self.roleSelected(r))
            self.buttons.append(button)
            right_layout.addWidget(button)

        layout.addLayout(right_layout)

        self.loadDescriptionFromFile("paragraphs/main_description.txt")

    #stop watch
    def startStopwatch(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # Update the timer every second.
            self.startStopButton.setText('Pause')
        else:
            self.timer.stop()
            self.startStopButton.setText('Continue')

    def updateStopwatch(self):
        self.elapsedTime += 1
        elapsedTimeString = '{:02d}:{:02d}:{:02d}'.format(self.elapsedTime // 3600, (self.elapsedTime % 3600 // 60), self.elapsedTime % 60)
        self.stopwatchLabel.setText(elapsedTimeString)

    def resetStopwatch(self):
        self.timer.stop()
        self.elapsedTime = 0
        self.stopwatchLabel.setText('00:00:00')
        self.startStopButton.setText('Start')

    #description of the main window
    def loadDescriptionFromFile(self, filename):
        try:
            with open(filename, "r") as file:
                description = file.read()
                self.descriptionLabel1.setText(description)
                self.descriptionLabel1.setWordWrap(True)
                self.descriptionLabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        except FileNotFoundError:
            print("Description file not found.")

    def speakDescription(self):
        """Reads the content of `descriptionLabel1` aloud."""
        text = self.descriptionLabel1.text()
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def roleSelected(self, selectedRole):
        # Assume the existence of a class FirestoreApp
        self.firestore_window = FirestoreApp(selectedRole, self)
        self.firestore_window.show()
        self.firestore_window.showFullScreen()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskReplicatorApp()
    ex.showFullScreen()
    sys.exit(app.exec_())


import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
import time
import subprocess

# Initialize Firebase
cred = credentials.Certificate('firebase/bci-research-77b3d-02a9edb61fd4.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class FirestoreApp(QWidget):
    def __init__(self, selectedRole, parent=None, timer=None):
        super().__init__()
        self.selectedRole = selectedRole
        self.parent = parent  # Reference to TaskReplicatorApp
        self.timer = QTimer(timer)  # Receive the timer instance
        self.elapsedTime = 0  # Keep track of the elapsed time
        self.initUI()
        self.startStopwatch()

    def initUI(self):
        self.setWindowTitle("Task Replicator")
        self.setGeometry(100, 100, 600, 400)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background1.png")))  # Ensure you have this image
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Back button
        self.backButton = QPushButton('Back', self)
        self.backButton.clicked.connect(self.goBack)
        self.backButton.setFont(QFont('Arial', 12))
        self.backButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
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

        add_user_button = QPushButton('Add User', self)
        add_user_button.clicked.connect(self.addUser)
        add_user_button.setFont(QFont('Arial', 12))
        add_user_button.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        layout.addWidget(add_user_button)

        # Title space to display selected role
        self.titleLabel = QLabel(self.selectedRole, self)
        self.titleLabel.setFont(QFont('Arial', 18))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: white; border-radius: 15px; padding: 20px; background-color: rgba(0, 0, 0, 150);")
        layout.addWidget(self.titleLabel)

        # Read and display the paragraph based on the selected role
        paragraph_label = QLabel("", self)
        paragraph_label.setAlignment(Qt.AlignJustify)
        paragraph_label.setWordWrap(True)
        paragraph_label.setFont(QFont('Arial', 12))
        paragraph_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 20px;")
        layout.addWidget(paragraph_label)

        # Read paragraph from file
        paragraph_file_path = os.path.join("paragraphs", f"{self.selectedRole.lower()}.txt")
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
        difficulty_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        difficulty_layout.addWidget(difficulty_label)
        
        self.difficulty_entry = QLineEdit(self)
        self.difficulty_entry.setFont(QFont('Arial', 12))
        self.difficulty_entry.setStyleSheet("padding: 10px; border-radius: 15px;")
        difficulty_layout.addWidget(self.difficulty_entry)
        layout.addLayout(difficulty_layout)

        self.addButton = QPushButton('Add Data to Firestore', self)
        self.addButton.clicked.connect(self.addDataToFirestore)
        self.addButton.setFont(QFont('Arial', 12))
        self.addButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")

        self.statusLabel = QLabel('', self)
        self.statusLabel.setFont(QFont('Arial', 12))
        self.statusLabel.setStyleSheet("color: white;")

        layout.addWidget(self.addButton)
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
    
    def addDataToFirestore(self):
        user_input = self.difficulty_entry.text()
        if user_input:
            doc_ref = db.collection(u'sample_data').document(self.user_id_entry.text())
            doc_ref.set({'hardness_level': int(user_input)})
            self.statusLabel.setText("Difficulty level added to Firestore")
            self.difficulty_entry.clear()

            # Modify the field name to adhere to Firestore's naming conventions
            elapsed_time_key = "nuclear_physics_description_read_time"

            # Add the elapsed time to Firestore in seconds
            doc_ref.update({elapsed_time_key: self.elapsedTime})
        
    # Stopwatch methods
    def startStopwatch(self):
        if self.timer and not self.timer.isActive():
            self.timer.start(1000)  # Update the timer every second.

    def updateStopwatch(self):
        self.elapsedTime += 1
        elapsedTimeString = '{:02d}:{:02d}:{:02d}'.format(self.elapsedTime // 3600, (self.elapsedTime % 3600 // 60), self.elapsedTime % 60)
        self.stopwatchLabel.setText(elapsedTimeString)

    @pyqtSlot()
    def goToNextPage(self):
        # Switch to the third page
        self.close()  # Ensure the current PyQt5 window is closed.
        QApplication.quit()  # Try to quit the application properly
        subprocess.Popen(["python", "thirdpage.py"])  # Start the third page

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Create a QTimer object
    timer = QTimer()
    ex = FirestoreApp("Tester", timer=timer)  # Ensure you pass a valid role or modify this accordingly
    timer.timeout.connect(ex.updateStopwatch)
    ex.showMaximized()
    sys.exit(app.exec_())

import tkinter as tk
import random
from PIL import Image, ImageTk
import platform

class DraggableCard(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, padx=10, pady=5, font=("Arial", 12), **kwargs)
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind("<ButtonRelease-1>", self.on_drag_release)
        self._drag_start_x = 0
        self._drag_start_y = 0
        self.original_x = 0
        self.original_y = 0
        self.cage = None
        self.locked = False

    def on_drag_start(self, event):
        if not self.locked:
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self.original_x = self.winfo_x()
            self.original_y = self.winfo_y()

    def on_drag_motion(self, event):
        if not self.locked:
            x = self.winfo_x() - self._drag_start_x + event.x
            y = self.winfo_y() - self._drag_start_y + event.y
            self.place(x=x, y=y)

    def on_drag_release(self, event):
        if not self.locked:
            self.snap_to_cage()

    def snap_to_cage(self):
        if not self.locked:
            closest_cage = None
            min_distance = float("inf")
            for cage in self.master.cages:
                if not cage[4] and cage[2] < self.winfo_y() < cage[3]:
                    distance = abs(self.winfo_x() - cage[0])
                    if distance < min_distance:
                        min_distance = distance
                        closest_cage = cage
            if closest_cage:
                self.place(x=closest_cage[0] + (closest_cage[1] - closest_cage[0]) // 2 - self.winfo_reqwidth() // 2,
                           y=closest_cage[2] + (closest_cage[3] - closest_cage[2]) // 2 - self.winfo_reqheight() // 2)
                self.cage = closest_cage
                self.master.arrange_cards_in_cage(self)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Draggable Cards")
        self.fullScreenState = False
        self.geometry('400x300')
        self.bind("<F11>", self.toggleFullScreen)
        self.bind("<Escape>", self.quitFullScreen)
        self.toggleFullScreen(None)

        # Load background image
        self.background_image = Image.open("images/background1.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Set background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list
        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 10))
        self.order_label.place(x=self.winfo_screenwidth() - 100, y=10)
        self.lock_button = tk.Button(self, text="Lock Cages", command=self.lock_cages, font=("Arial", 10), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - 100, y=40)
        self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.attributes("-fullscreen", self.fullScreenState)
        self.geometry('400x300')

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.attributes("-fullscreen", self.fullScreenState)
        self.geometry('400x300')

    def lock_cages(self):
        for cage in self.cages:
            cage_list = list(cage)  # Convert tuple to list
            cage_list[4] = True  # Lock all cages
            self.cages[self.cages.index(cage)] = tuple(cage_list)  # Convert list back to tuple
        self.lock_button.config(state="disabled", bg="#333333")  # Disable lock button
        self.unlock_button.config(state="normal", bg="#333333")  # Enable unlock button
        for card in self.cards:
            card.locked = True
        self.calculate_percentage()

    def unlock_cages(self):
        for cage in self.cages:
            cage_list = list(cage)  # Convert tuple to list
            cage_list[4] = False  # Unlock all cages
            self.cages[self.cages.index(cage)] = tuple(cage_list)  # Convert list back to tuple
        self.unlock_button.config(state="disabled", bg="#333333")  # Disable unlock button
        self.lock_button.config(state="normal", bg="#333333")  # Enable lock button
        for card in self.cards:
            card.locked = False
        self.calculate_percentage()

    def create_cages(self):
        cage_height = int(self.winfo_screenheight() * 0.1)
        cage_width = 400
        num_cages = 5
        for i in range(num_cages):
            cage_y = i * (self.winfo_screenheight() // num_cages)
            cage = (10, 10 + cage_width, cage_y, cage_y + cage_height, False)  # Add lock status to cage tuple
            self.create_curved_cage(cage_width, cage_height, cage_y)
            self.cages.append(cage)

    def create_curved_cage(self, width, height, y):
        canvas = tk.Canvas(self, width=width, height=height, bg="#333333")
        canvas.place(x=10, y=y)

        # Get the window ID of the canvas
        window_id = canvas.winfo_id()

        # Check the platform to set transparency
        if platform.system() == "Windows":
            # Set transparency for Windows using the window ID
            from ctypes import windll
            windll.dwmapi.DwmSetWindowAttribute(window_id, 2, 0, 2)  # Enable transparency

        elif platform.system() == "Darwin":
            # Set transparency for macOS using the window ID
            # Example: set the alpha value to 0.5 (50% transparency)
            from ctypes import c_void_p, c_float, c_int, POINTER, Structure, windll
            kCGWindowAlpha = 5
            kCGNullWindowID = 0
            kCGWindowListOptionAll = 0
            kCGWindowImageOptionDefault = 0

            # Define necessary structures and types
            class CGRect(Structure):
                _fields_ = [("origin", c_void_p), ("size", c_void_p)]

            CGFloat = c_float
            CFIndex = c_int

            # Get necessary functions from CoreGraphics framework
            CGWindowListCopyWindowInfo = windll.CoreGraphics.CGWindowListCopyWindowInfo
            CGWindowListCreateImage = windll.CoreGraphics.CGWindowListCreateImage
            CGWindowListCreateImage.restype = c_void_p
            CGWindowListCreateImage.argtypes = [CGRect, c_int, c_int, c_int]

            # Set transparency by calling macOS-specific functions
            image = CGWindowListCreateImage(CGRect(), kCGWindowListOptionAll, kCGNullWindowID, kCGWindowImageOptionDefault)
            canvas.create_image(0, 0, image=image, anchor=tk.NW)

        elif platform.system() == "Linux":
            # Set transparency for Linux using the window ID
            # Note: Linux transparency might require additional configuration
            pass

    def create_cards(self):
        card_texts = ["Apple", "Banana", "Orange", "Grape", "guvava"]
        random.shuffle(card_texts)
        num_cards = len(card_texts)
        right_margin = 20  # Set the margin from the right side of the screen
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self, text=card_text, bg="#4c4c4c", fg="white")
            # Place the card on the right-hand side with a margin
            card.place(x=self.winfo_screenwidth() - right_margin - card.winfo_reqwidth() * 5,
                    y=random.randint(90, 400))  
            self.cards.append(card)

    def calculate_percentage(self):
        correct_order = ["Apple", "Banana", "Orange", "Grape", "guvava"]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        self.order_label.config(text=f"Order: {percentage:.2f}%", fg="white")

    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

       
