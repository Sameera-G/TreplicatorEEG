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
from firebase import Firebase
from retrive_role_id import RetriveRoleId
from draggable_cards import DraggableCard
from utilities_view import create_cages, toggle_full_screen, quit_full_screen, create_curved_cage, load_text_from_file

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
        title_label = tk.Label(title_frame, text="Curriculum Development - Arrange the Learning Objctives in Correct Order", fg="white", bg="black", font=("Arial", 16, "bold"))
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list

        # Load text from file
        self.load_text_from_file("paragraphs/teacher_curriculum_description.txt", 0.07, 0.35)

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_cages, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.8)
        
        self.create_cages(5, 0.07, 0.04, 0.37)
        self.create_cards()

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

    def toggleFullScreen(self):
        toggle_full_screen(self)

    def quitFullScreen(self):
        quit_full_screen(self)

    def lock_cages(self):
        for cage in self.cages:
            cage_list = list(cage)  # Convert tuple to list
            cage_list[4] = True  # Lock all cages
            self.cages[self.cages.index(cage)] = tuple(cage_list)  # Convert list back to tuple
        self.lock_button.config(state="disabled", bg="#333333")  # Disable lock button
        #self.unlock_button.config(state="normal", bg="#333333")  # Enable unlock button
        for card in self.cards:
            card.locked = True
        self.calculate_percentage()
        #go to next page after 5 seconds
        self.after(5000, self.goToNextPage)

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
    
    def create_cages(self, num_cages, top_margin_percentage, bottom_margin_percentage, left_margin_percentage):
        create_cages(self, num_cages, top_margin_percentage, bottom_margin_percentage, left_margin_percentage)

    def create_curved_cage(self, width, height, x, y):
        create_curved_cage(self, width, height, x, y)

    def create_cards(self):
        card_texts = [
            "Understand the basic structure of the atom and \nthe discovery of the nucleus.",
            "Have a foundational knowledge of nuclear forces, particularly \nthe strong nuclear force, and their role in nucleon binding.",
            "Grasp the concepts of radioactivity, nuclear fission, \nand nuclear fusion and their applications.",
            "Comprehend the models of nuclear structure, \nincluding the liquid drop model and the shell model.",
            "Appreciate the impact of nuclear physics on technology, \nenergy, medicine, and environmental management."
        ]
        random.shuffle(card_texts)
        num_cards = len(card_texts)
        right_margin = 20  # Set the margin from the right side of the screen
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self, text=card_text, bg="#4c4c4c", fg="white", font=("Arial", 10))
            # Place the card on the right-hand side with a margin
            card.place(
                x=self.winfo_screenwidth() - right_margin - card.winfo_reqwidth() * 1,
                y=random.randint(90, 400)
            )  
            self.cards.append(card)

    def calculate_percentage(self):
        correct_order = [
            "Understand the basic structure of the atom and \nthe discovery of the nucleus.",
            "Have a foundational knowledge of nuclear forces, particularly \nthe strong nuclear force, and their role in nucleon binding.",
            "Grasp the concepts of radioactivity, nuclear fission, \nand nuclear fusion and their applications.",
            "Comprehend the models of nuclear structure, \nincluding the liquid drop model and the shell model.",
            "Appreciate the impact of nuclear physics on technology, \nenergy, medicine, and environmental management."
        ]
        total_correct = 0
        total_cards = 5 #len(correct_order)
        for i, cage in enumerate(self.cages):
            cards_in_cage = [
                card for card in self.cards if cage[2] < card.winfo_y() < cage[3]
            ]
            if len(cards_in_cage) == 1:
                card_text = cards_in_cage[0].cget("text")
                if card_text == correct_order[i]:
                    total_correct += 1
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")
        return percentage

    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

    def goToNextPage(self):
        # Calculate percentage
        percentage = self.calculate_percentage()
        # Update stopwatch and get the time taken
        time_taken = self.update_stopwatch()
        # Example usage: Adding data to Firestore

        main_data = {
            'Accuracy_Percentage_curriculum_development': percentage,
            # Add more fields as needed
        }

        # Data for the nested "times" collection
        time_data = {
            'Time_taken_for_curriculum_development': time_taken,
        }
        # Update the main collection (selected_role/user_id)
        firebase.update_data(self.selected_role, self.user_id, main_data)
        # Add to the nested "times" collection using the new method
        firebase.add_time_data(self.selected_role, self.user_id, time_data)
        
        # Show the splash screen
        pixmap = QPixmap("images/loading.jpg")
        splash = SplashScreen(pixmap)
        splash.show()

        #self.close()  # Ensure the current PyQt5 window is closed.
        self.destroy()
        self.openNextPage()

        # Delay before showing the next page (simulated loading time)
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)  # Adjust the delay as needed
        loop.exec_()

    def openNextPage(self):
        subprocess.Popen(["python", "teacher_pages/fourthpage_t.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()
    # Retrieve data
    retriveroleid = RetriveRoleId()
    selected_role, user_id = retriveroleid.retrieve_data()
    window = MainWindow(selected_role, user_id, firebase)  # Pass the firebase object here
    window.mainloop()
    sys.exit(app.exec_())


       
