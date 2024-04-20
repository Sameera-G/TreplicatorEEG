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
from firebase import Firebase
from retrive_role_id import RetriveRoleId

# Splash screen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

class DraggableCard(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, padx=10, pady=5, **kwargs)
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
        self.toggleFullScreen(None)

        # Load background image
        self.background_image = Image.open("images/background1.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Set background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a title label with a black transparent ribbon background
        title_frame = tk.Frame(self, bg="black", bd=0, highlightthickness=0)
        title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        title_label = tk.Label(title_frame, text="Code Testing (Security Test Cases) - Arrange the testing Code Snippets in Correct Order", fg="white", bg="black", font=("Arial", 16, "bold"))
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list

        # Load text from file
        self.load_text_from_file("software_eng_pages/paragraphs_se/nine_page_test.txt")

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_cages, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.8)
        #self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        #self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()

    def load_text_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()

                # Create a canvas for curved corners
                canvas = tk.Canvas(self, bg="#1f1f1f", highlightbackground="#1f1f1f", highlightthickness=0)
                canvas.place(x=10, y=self.winfo_screenheight() * 0.07, relwidth=0.25, relheight=0.9)

                # Add curved corners to the canvas
                self.create_curved_rectangle(canvas, 0, 0, canvas.winfo_width(), canvas.winfo_height(), 50)

                # Create the text widget
                text_widget = tk.Text(canvas, wrap="word", bg="#1f1f1f", fg="white", font=("Arial", 10),
                                    highlightbackground="#1f1f1f", highlightthickness=5, padx=10, pady=10)
                text_widget.insert("1.0", content)
                text_widget.place(relwidth=1, relheight=1)
                text_widget.config(state="disabled")  # Make the text area read-only
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

        # Create stopwatch
        self.stopwatch_label = tk.Label(self, text="", bg="#1f1f1f", fg="white", font=("Arial", 16))
        self.stopwatch_label.place(x=self.winfo_screenwidth() - 70, y=60)
        # Create stopwatch instance
        self.stopwatch = StopWatch()
        # Update stopwatch label every second
        self.update_stopwatch()

    def update_stopwatch(self):
        self.stopwatch_label.config(text=self.stopwatch.elapsedTime)
        self.after(1000, self.update_stopwatch)

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
        top_margin_percentage = 0.07  # 5% space from the top of the screen
        space_between_cages = 2  # Adjust this value as needed
        cage_height = int((self.winfo_screenheight() - top_margin_percentage) * 0.9 / 3) - 2
        num_cages_first_column = 3
        num_cages_second_column = 0
        left_margin_percentage = 0.27  # 22% space from the left side of the screen

        # Calculate the width of the cages after leaving space on the left
        cage_width = int(self.winfo_screenwidth() * (left_margin_percentage * 1.2))
        cage_x_start_first_column = int(self.winfo_screenwidth() * left_margin_percentage)  # Starting X position for first column
        cage_x_start_second_column = cage_x_start_first_column + cage_width  # Starting X position for second column

        # Create cages in the first column
        for i in range(num_cages_first_column):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage) + i * (cage_height + space_between_cages)
            cage = (cage_x_start_first_column, cage_x_start_first_column + cage_width, cage_y, cage_y + cage_height, False)
            self.create_curved_cage(cage_width, cage_height, cage_x_start_first_column, cage_y)
            self.create_cage_number(cage_x_start_first_column + cage_width - 20, cage_y + 10, i + 1)
            self.cages.append(cage)

        # Create cages in the second column
        for i in range(num_cages_second_column):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage) + i * (cage_height + space_between_cages)
            cage = (cage_x_start_second_column, cage_x_start_second_column + cage_width, cage_y, cage_y + cage_height, False)
            self.create_curved_cage(cage_width, cage_height, cage_x_start_second_column, cage_y)
            self.create_cage_number(cage_x_start_second_column + cage_width - 20, cage_y + 10, i + 1 + num_cages_first_column)
            self.cages.append(cage)

    def create_cage_number(self, x, y, number):
        cage_number = tk.Label(self, text=str(number), bg="#4c4c4c", fg="white", font=("Arial", 10))
        cage_number.place(x=x, y=y)

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
        # Define the user registration code snippet
        one = (
            "Simulate registration form data with SQL injection payload:\n"
            "   - Prepare registration form data:\n"
            "       - Define a dictionary containing the username ('testuser'), email ('test@example.com'), \nand a potential SQL injection payload ('' OR '1'='1').\n"
            "   - The SQL injection payload attempts to bypass the registration form validation."
        )
        two = (
            "Send a POST request to the registration route with form data:\n"
            "   - Use the Flask test client to send a POST request to the '/register' route of the application.\n"
            "   - Include the registration form data with the SQL injection payload in the request payload.\n"
        )
        three = (
            "Verify the prevention of SQL injection:\n"
            "   - Check the response status code:\n"
            "       - If the status code is 400, the registration failed due to prevention of SQL injection.\n"
            "   - Check the response message:\n"
            "       - If the message indicates failure ('Form validation failed'), the test passes.\n"
            "Expected Outcome:- The test should pass, indicating that the application successfully \nprevents SQL injection attacks during user registration."
        )
        card_texts = [
            one,
            two,
            three
        ]

        random.shuffle(card_texts)
        num_cards = len(card_texts)
        right_margin = 20  # Set the margin from the right side of the screen
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self, text=card_text, bg="#4c4c4c", fg="white", font=("Arial", 8), justify="left")
            # Place the card on the right-hand side with a margin
            card.place(
                x=self.winfo_screenwidth() - right_margin - card.winfo_reqwidth() * 1,
                y=random.randint(90, 400)
            )  
            self.cards.append(card)

    def calculate_percentage(self):
        # Define the user registration code snippet
        one = (
            "Simulate registration form data with SQL injection payload:\n"
            "   - Prepare registration form data:\n"
            "       - Define a dictionary containing the username ('testuser'), email ('test@example.com'), \nand a potential SQL injection payload ('' OR '1'='1').\n"
            "   - The SQL injection payload attempts to bypass the registration form validation."
        )
        two = (
            "Send a POST request to the registration route with form data:\n"
            "   - Use the Flask test client to send a POST request to the '/register' route of the application.\n"
            "   - Include the registration form data with the SQL injection payload in the request payload.\n"
        )
        three = (
            "Verify the prevention of SQL injection:\n"
            "   - Check the response status code:\n"
            "       - If the status code is 400, the registration failed due to prevention of SQL injection.\n"
            "   - Check the response message:\n"
            "       - If the message indicates failure ('Form validation failed'), the test passes.\n"
            "Expected Outcome:- The test should pass, indicating that the application successfully \nprevents SQL injection attacks during user registration."
        )
        correct_order = [
            one,
            two,
            three
        ]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")
        return percentage

    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

    def goToNextPage(self):
        # Calculate percentage
        percentage = self.lock_boxes()
        # Update stopwatch and get the time taken
        time_taken = self.update_stopwatch()
        # Example usage: Adding data to Firestore
        data = {
            'Accuracy_Percentage_code_testing_Security': percentage,
            'Time_taken_to_answer_code_testing_Security': time_taken,
            # Add more fields as needed
        }

        firebase.update_data(self.selected_role, self.user_id, data)
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
        subprocess.Popen(["python", "software_eng_pages/sixthse.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()
    # Retrieve data
    retriveroleid = RetriveRoleId()
    selected_role, user_id = retriveroleid.retrieve_data()
    window = MainWindow(selected_role, user_id, firebase)
    window.mainloop()
    sys.exit(app.exec_())

       
