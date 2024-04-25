import sys
import tkinter as tk
import random
import json
from PIL import Image, ImageTk
import platform
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QApplication, QWidget, QSplashScreen
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QEventLoop
import subprocess
sys.path.append('I:/Research/TreplicatorEEG/utilities_files')
from stop_watch import StopWatch
from firebase_func import Firebase
from retrive_role_id import RetriveRoleId
from utilities_view import toggle_full_screen, quit_full_screen, create_curved_cage, load_text_from_file

# Splash screen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

class MainWindow(tk.Tk):
    def __init__(self, selected_role, user_id, firebase):
        super().__init__()
        self.title("Draggable Cards")
        self.selected_role = selected_role
        self.user_id = user_id
        self.firebase = firebase
        self.fullScreenState = False
        self.geometry('400x300')
        self.bind("<F11>", self.toggleFullScreen)
        self.bind("<Escape>", self.quitFullScreen)
        self.toggleFullScreen()

        # Load background image
        self.background_image = Image.open("images/background1.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Set background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a title label with a black transparent ribbon background
        title_frame = tk.Frame(self, bg="black", bd=0, highlightthickness=0)
        title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        title_label = tk.Label(title_frame, text="Authentication Activities Priority Matrix - Type Priority (high/medium) in Correct Order", fg="white", bg="black", font=("Arial", 16, "bold"))
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Load text from file
        self.load_text_from_file("software_eng_pages/paragraphs_se/softeeng_task_description.txt", 0.07, 0.25)

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.text_boxes = []
        self.correct_order = ["high", "high", "high", "high", "medium", "high", "medium", "medium", "high", "high"]  # Correct order of strings
        self.create_text_boxes()

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_boxes, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.8)

        # Create stopwatch
        self.stopwatch_label = tk.Label(self, text="", bg="#1f1f1f", fg="white", font=("Arial", 16))
        self.stopwatch_label.place(x=self.winfo_screenwidth() - 100, y=100)
        # Create stopwatch instance
        self.stopwatch = StopWatch()
        # Update stopwatch label every second
        self.update_stopwatch()

    def update_stopwatch(self):
        self.stopwatch_label.config(text=self.stopwatch.elapsedTime)
        self.after(1000, self.update_stopwatch)
        return self.stopwatch.elapsedTime
    
    def load_text_from_file(self, file_path, margin_from_top, relwidth):
        load_text_from_file(self, file_path, margin_from_top, relwidth)

    def create_curved_rectangle(self, canvas, x1, y1, x2, y2, r):
        canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1 + r, y1, x2 - r, y2, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1, y1 + r, x2, y2 - r, outline="", fill="#1f1f1f")
    
    def toggleFullScreen(self):
        toggle_full_screen(self)

    def quitFullScreen(self):
        quit_full_screen(self)

    def lock_boxes(self):
        total_correct = 0
        total_entries = 0  # Total number of text entry boxes
        for i in range(len(self.text_boxes)):
            if isinstance(self.text_boxes[i], tk.Entry):  # Check if it's an Entry widget
                total_entries += 1
                if self.text_boxes[i].get() == self.correct_order[total_entries - 1]:  # Match with correct_order
                    total_correct += 1
        percentage = (total_correct / total_entries) * 100
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")
        self.lock_button.config(state="disabled", bg="#333333")  # Disable lock button
        # Go to next page after 5 seconds
        self.after(5000, self.goToNextPage)
        return percentage


    def create_text_boxes(self):
        top_margin_percentage = 0.07  # 0.05% space from the top of the screen
        bottom_margin_percentage = 0.25  # 0.05% space from the bottom of the screen
        tb_height = int((self.winfo_screenheight() - top_margin_percentage - bottom_margin_percentage) / 5)
        
        num_rows = 5
        num_columns = 3
        left_margin_percentage = 0.3  # 30% space from the left side of the screen
        space_between_cages = 2

        # Calculate the width of the text boxes after leaving space on the left
        tb_width = int((self.winfo_screenwidth() * (1 - left_margin_percentage) / 1.5) / (num_columns))
        tb_x_start = int(self.winfo_screenwidth() * left_margin_percentage)  # Starting X position
        
        # List of sentences for the label boxes
        sentences = [
            "Create a new account",
            "Log in to existing\naccount",
            "Password reset\nfunctionality",
            "Account management\nfor administrators",
            "Secure implementation\nof user authentication"
        ]

        # Labels for the top of each column
        column_labels = ["Importance\ntype high, medium or low", "Urgency\ntype high, medium or low", "User Story"]

        # Create label boxes for the top row
        for j in range(num_columns):
            top_label_y = int(self.winfo_screenheight() * top_margin_percentage)
            top_label = tk.Label(self, text=column_labels[j], bg="#333333", fg="white", font=("Arial", 12), highlightthickness=2, highlightbackground="#FFFFFF", highlightcolor="#FFFFFF")
            top_label.place(x=tb_x_start + j * tb_width, y=top_label_y, width=tb_width, height=tb_height*0.5)

        # Create text boxes and label boxes
        for i in range(num_rows):
            for j in range(num_columns):
                x = tb_x_start + j * tb_width
                y = int((self.winfo_screenheight() * top_margin_percentage) + tb_height + space_between_cages) + (i * (tb_height))
                if j < num_columns - 1:  # Create regular text boxes for the first two columns
                    text_box = tk.Entry(self, bg="#333333", fg="white", font=("Arial", 12), highlightbackground="#FFFFFF", highlightthickness=2)
                else:  # Create label boxes for the last column
                    text_box = tk.Label(self, text=sentences[i], wraplength=tb_width, justify="left", bg="#333333", fg="white", font=("Arial", 12), highlightthickness=2, highlightbackground="#FFFFFF", highlightcolor="#FFFFFF")
                text_box.place(x=x, y=y, width=tb_width, height=tb_height/2)
                self.text_boxes.append(text_box)

        # Print the length of self.text_boxes for debugging
        print("Number of text boxes created:", len(self.text_boxes))

    def goToNextPage(self):
        # Calculate percentage
        percentage = self.lock_boxes()
        # Update stopwatch and get the time taken
        time_taken = self.update_stopwatch()
        # Example usage: Adding data to Firestore
        main_data = {
            'Accuracy_Percentage_user_matrix': percentage,
            # Add more fields as needed
        }

        # Data for the nested "times" collection
        time_data = {
            'Time_taken_to_answer_user_matrix': time_taken,
        }
        # Update the main collection (selected_role/user_id)
        firebase.update_data(self.selected_role, self.user_id, main_data)
        # Add to the nested "times" collection using the new method
        firebase.add_time_data(self.selected_role, self.user_id, time_data)
        
        # Show the splash screen
        pixmap = QPixmap("images/loading.jpg")
        splash = SplashScreen(pixmap)
        splash.show()

        self.destroy()  # Close the current tkinter window
        self.openNextPage()

        # Delay before showing the next page (simulated loading time)
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()

    def openNextPage(self):
        subprocess.Popen(["python", "software_eng_pages/fifthse.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()
    # Retrieve data
    retriveroleid = RetriveRoleId()
    selected_role, user_id = retriveroleid.retrieve_data()
    window = MainWindow(selected_role, user_id, firebase)
    window.mainloop()
    sys.exit(app.exec_())
