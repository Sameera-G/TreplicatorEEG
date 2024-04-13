from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
import pyttsx3
from PyQt5.QtCore import QTimer

class StopWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speech_engine = pyttsx3.init()  # Initialize the speech synthesis engine.
        self.timer = QTimer(self)  # Instantiate QTimer
        self.timer.timeout.connect(self.updateStopwatch)
        self.elapsedTime = 0  # Keep track of the elapsed time
        self.startStopwatch()

    def initUI(self):
        style_1 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;"

        left_layout = QVBoxLayout()

        #stop watch
        self.stopwatchLabel = QLabel('00:00:00', self)
        self.stopwatchLabel.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.stopwatchLabel)

        self.startStopButton = QPushButton('Start', self)
        self.startStopButton.setStyleSheet(style_1)
        self.startStopButton.clicked.connect(self.startStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)  # Convert to integer
        button_height = int(self.startStopButton.sizeHint().height())  # Convert to integer
        self.startStopButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.startStopButton)

        self.resetButton = QPushButton('Reset', self)
        self.resetButton.setStyleSheet(style_1)
        self.resetButton.clicked.connect(self.resetStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)
        button_height = int(self.resetButton.sizeHint().height())  
        self.resetButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.resetButton)


    #stop watch
    def startStopwatch(self):
        if not self.timer.isActive():
            self.timer.start(1000) 
            self.startStopButton.setText('Pause')
        else:
            self.timer.stop()
            self.startStopButton.setText('Continue')

    def updateStopwatch(self):
        self.elapsedTime += 1
        elapsed_time_string = '{:02d}:{:02d}:{:02d}'.format(self.elapsedTime // 3600, (self.elapsedTime % 3600 // 60), self.elapsedTime % 60)
        self.stopwatchLabel.setText(elapsed_time_string)

    def resetStopwatch(self):
        self.timer.stop()
        self.elapsedTime = 0
        self.stopwatchLabel.setText('00:00:00')
        self.startStopButton.setText('Start')