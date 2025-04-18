import sys
import tkinter as tk
import random
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
from draggable_cards import DraggableCard
from utilities_view import toggle_full_screen, quit_full_screen, create_curved_cage, load_text_from_file

# Splash screen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Draggable Cards")
        self.firebase = firebase
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

        # Load text from file
        self.load_text_from_file("paragraphs/teacher_curriculum_description.txt", 0.07, 0.25)  # Replace 'your_text_file.txt' with your file path

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_cages, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.8)
        #self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        #self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()


    def create_curved_rectangle(self, canvas, x1, y1, x2, y2, r):
        canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1 + r, y1, x2 - r, y2, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1, y1 + r, x2, y2 - r, outline="", fill="#1f1f1f")

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

    def create_cages(self):
        cage_height = int(self.winfo_screenheight() * 0.9/5 * 0.9)
        num_cages = 5
        left_margin_percentage = 0.3  # 30% space from the left side of the screen

        # Calculate the width of the cages after leaving space on the left
        cage_width = int((self.winfo_screenwidth() * (1 - left_margin_percentage)) / num_cages) * 2
        cage_x_start = int(self.winfo_screenwidth() * left_margin_percentage)  # Starting X position

        top_margin_percentage = 0.05  # 0.05% space from the top of the screen
        bottom_margin_percentage = 0.05  # 0.05% space from the bottom of the screen
        available_height = self.winfo_screenheight() * (1 - top_margin_percentage - bottom_margin_percentage)

        for i in range(num_cages):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage) + i * (available_height // num_cages)
            cage = (cage_x_start, cage_x_start + cage_width, cage_y, cage_y + cage_height, False)  # Add lock status to cage tuple
            self.create_curved_cage(cage_width, cage_height, cage_x_start, cage_y)
            self.cages.append(cage)

    def create_curved_cage(self, width, height, x, y):
        canvas = tk.Canvas(self, width=width, height=height, bg="#333333")
        canvas.place(x=x, y=y)

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
            #kcgwindow_alpha = 5
            kcgnull_window_id = 0
            kcgwindow_list_option_all = 0
            kcgwindow_image_option_default = 0

            # Define necessary structures and types
            class CGRect(Structure):
                _fields_ = [("origin", c_void_p), ("size", c_void_p)]

            #CGFloat = c_float
            #CFIndex = c_int

            # Get necessary functions from CoreGraphics framework
            #cgwindow_list_copy_window_info = windll.CoreGraphics.cgwindow_list_copy_window_info
            cgwindow_list_create_image = windll.CoreGraphics.cgwindow_list_create_image
            cgwindow_list_create_image.restype = c_void_p
            cgwindow_list_create_image.argtypes = [CGRect, c_int, c_int, c_int]

            # Set transparency by calling macOS-specific functions
            image = cgwindow_list_create_image(CGRect(), kcgwindow_list_option_all, kcgnull_window_id, kcgwindow_image_option_default)
            canvas.create_image(0, 0, image=image, anchor=tk.NW)

        elif platform.system() == "Linux":
            # Set transparency for Linux using the window ID
            # Note: Linux transparency might require additional configuration
            pass


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
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        # Add newline character (\n) for multiline text
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")


    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

    def goToNextPage(self):
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
        subprocess.Popen(["python", "teacher_pages/fourthpage.py"])  # Start the third page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()
    window = MainWindow()
    window.mainloop()
    sys.exit(app.exec_())

       
