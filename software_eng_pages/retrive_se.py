import sys
import os
import json
import firebase_admin
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush

# Initialize Firebase
sys.path.append("I:/Research/TreplicatorEEG/utilities_files")
from firebase import Firebase
from retrive_role_id import RetriveRoleId

class FirestoreApp(QWidget):
    def __init__(self, selected_role, user_id, firebase, parent=None, timer=None):
        super().__init__()
        self.selected_role = selected_role
        self.user_id = user_id
        self.firebase = firebase
        self.parent = parent  # Reference to TaskReplicatorApp
        self.timer = QTimer(timer)  # Receive the timer instance
        self.elapsedTime = 0  # Keep track of the elapsed time
        self.initUI()

    def initUI(self):
        style_1 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;"
        style_2 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 20px;"

        self.setWindowTitle("Task Replicator")
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background1.png")))
        self.setPalette(palette)

        # Create a vertical layout for the title, tables, and averages
        v_layout = QVBoxLayout()

        # Title text for the application
        title = QLabel(
            f"Data for {self.selected_role} - {self.user_id} \nThe values mentioned below should not be considered as an indicator of your performance.\nThey were accumulated only for comparison purposes with the EEG signal. \n THANK YOU FOR PARTICIPATING IN THE STUDY!"
        )
        title.setFont(QFont("Helvetica", 18))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style_1)
        v_layout.addWidget(title)  # Add the title to the top of the vertical layout

        # Horizontal layout for the first table and the averages label
        h_layout = QHBoxLayout()

        # First QTableWidget displaying Firebase data from the main collection
        self.table1 = QTableWidget(self)
        self.table1.setColumnCount(2)  # Two columns: Field, Value
        self.table1.setHorizontalHeaderLabels(["Field", "Value"])
        self.table1.horizontalHeader().setStretchLastSection(True)  # Stretch the last column to fill space
        self.table1.setColumnWidth(0, 450)  # Increase the first column's width
        self.table1.setStyleSheet(
            "background-color: rgba(2, 2, 2, 150);"
            "border-radius: 15px;"
            "padding: 10px;"
            "color: white;"
        )
        self.table1.setFont(QFont("Helvetica", 12))
        self.table1.setFixedWidth(int(QApplication.desktop().screenGeometry().width() * 0.5))

        # Averages label in a transparent box
        self.averages_label = QLabel(self)
        self.averages_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150);" +
            "border-radius: 15px;" +
            "padding: 15px;" +
            "color: white;"
        )
        self.averages_label.setFont(QFont("Helvetica", 14))

        h_layout.addWidget(self.table1)  # Add the first table to the horizontal layout
        h_layout.addWidget(self.averages_label)  # Add the averages label box to the horizontal layout

        v_layout.addLayout(h_layout)  # Add the horizontal layout to the vertical layout

        # Second QTableWidget for Firebase data from the "times" collection
        self.table2 = QTableWidget(self)
        self.table2.setColumnCount(2)  # Two columns: Field, Value
        self.table2.setHorizontalHeaderLabels(["Field", "Value"])
        self.table2.horizontalHeader().setStretchLastSection(True)  # Stretch the last column
        self.table2.setColumnWidth(0, 450)
        self.table2.setStyleSheet(
            "background-color: rgba(2, 2, 2, 150);" +
            "border-radius: 15px;" +
            "padding: 10px;" +
            "color: white;"
        )
        self.table2.setFont(QFont("Helvetica", 12))
        self.table2.setFixedWidth(int(QApplication.desktop().screenGeometry().width() * 0.5))
        
        v_layout.addWidget(self.table2)  # Add the second table under the first one

        self.setLayout(v_layout)  # Use the vertical layout for the QWidget
        
        # Load data from Firebase and update the averages
        self.load_data_from_firebase()
        self.update_averages()  # Calculate and display the averages

    def load_data_from_firebase(self):
        try:
            # Load data from the main collection
            main_data = self.firebase.retrieve_data(self.selected_role, self.user_id)
            if main_data:
                self.table1.setRowCount(len(main_data))
                for row, (key, value) in enumerate(main_data.items()):
                    self.table1.setItem(row, 0, QTableWidgetItem(key))
                    self.table1.setItem(row, 1, QTableWidgetItem(str(value)))

            # Load data from the "times" collection
            times_data = self.firebase.retrieve_data(
                f"{self.selected_role}/{self.user_id}/times", self.user_id
            )
            if times_data:
                self.table2.setRowCount(len(times_data))
                for row, (key, value) in enumerate(times_data.items()):
                    self.table2.setItem(row, 0, QTableWidgetItem(key))
                    self.table2.setItem(row, 1, QTableWidgetItem(str(value)))

        except Exception as e:
            print("Error retrieving data from Firebase:", e)

    def update_averages(self):
        # Calculate the average values for the first table (percentage accuracy)
        sum_accuracy = 0
        count_accuracy = 0
        for row in range(self.table1.rowCount()):
            try:
                value = float(self.table1.item(row, 1).text())
                sum_accuracy += value
                count_accuracy += 1
            except ValueError:
                continue

        avg_accuracy = sum_accuracy / count_accuracy if count_accuracy > 0 else None

        # Calculate the average values for the second table (time consumed)
        sum_time = 0
        count_time = 0
        for row in range(self.table2.rowCount()):
            try:
                value = float(self.table2.item(row, 1).text())
                sum_time += value
                count_time += 1
            except ValueError:
                continue

        avg_time = sum_time / count_time if count_time > 0 else None

        # Update the label with the average values
        info_text = f"Average Percentage Accuracy: {avg_accuracy:.2f}%" if avg_accuracy else "Average Percentage Accuracy: N/A"
        info_text += f"\nAverage Time Consumed: {avg_time:.2f} seconds" if avg_time else "Average Time Consumed: N/A"
        
        self.averages_label.setText(info_text)  # Update the label with the calculated averages

# Main execution code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()  # Firebase initialization
    retriveroleid = RetriveRoleId()  # Custom role ID retrieval logic
    selected_role, user_id = retriveroleid.retrieve_data()  # Retrieve role and user ID
    
    ex = FirestoreApp(selected_role, user_id, firebase)  # Pass the Firebase instance
    ex.showFullScreen()  # Show the window in full-screen mode

    sys.exit(app.exec_())
