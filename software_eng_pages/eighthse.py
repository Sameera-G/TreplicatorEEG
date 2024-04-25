import sys
import tkinter as tk
import random
from PIL import Image, ImageTk
import platform
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
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
        title_label = tk.Label(title_frame, text="Code Testing (Negative Test Cases) - Arrange the testing Code Snippets in Correct Order", fg="white", bg="black", font=("Arial", 16, "bold"))
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list

        # Load text from file
        self.load_text_from_file("software_eng_pages/paragraphs_se/eighth_page_negative_test.txt", 0.07, 0.25)

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_cages, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - self.winfo_screenwidth() * 0.2, y=self.winfo_screenheight() * 0.8)
        #self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        #self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()

    def load_text_from_file(self, file_path, margin_from_top, relwidth):
        load_text_from_file(self, file_path, margin_from_top, relwidth)

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
        return self.stopwatch.elapsedTime

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
        cage_height = int((self.winfo_screenheight() - top_margin_percentage) * 0.9 / 4) - 2
        num_cages_first_column = 4
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
        create_curved_cage(self, width, height, x, y)

    def create_cards(self):
        # Define the user registration code snippet
        one = (
            "Set up the testing environment:\n"
            "    - Enable testing mode in the Flask application configuration.\n"
            "    - Configure the SQLAlchemy database URI to use an in-memory SQLite database."
        )
        two = (
            "Create a test user:\n"
            "   - Add a user record to the database with valid login credentials:\n"
            "       - Username: 'testuser'\n"
            "       - Email: 'test@example.com'\n"
            "       - Password: 'testpassword'\n"
        )
        three = (
            "Simulate the user login process with invalid password:\n"
            "   - Prepare login form data:\n"
            "       - Define a dictionary containing the username ('testuser') \nand an invalid password ('wrongpassword').\n"
            "   - Send a POST request to the login route ('/login') of the Flask application.\n"
            "   - Include the login form data in the request payload.\n"
        )
        four = (
            "Verify the login outcome:\n"
            "   - Check the response status code:\n"
            "       - If the status code is 401, the login failed due to invalid password.\n"
            "   - Check the response message:\n"
            "       - If the message indicates failure ('Invalid username or password'), the test passes.\n"
            "Expected Outcome:- The test should pass, indicating that the user \nlogin process fails correctly when an invalid password is provided."
        )
        card_texts = [
            one,
            two,
            three,
            four
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
            "Set up the testing environment:\n"
            "    - Enable testing mode in the Flask application configuration.\n"
            "    - Configure the SQLAlchemy database URI to use an in-memory SQLite database."
        )
        two = (
            "Create a test user:\n"
            "   - Add a user record to the database with valid login credentials:\n"
            "       - Username: 'testuser'\n"
            "       - Email: 'test@example.com'\n"
            "       - Password: 'testpassword'\n"
        )
        three = (
            "Simulate the user login process with invalid password:\n"
            "   - Prepare login form data:\n"
            "       - Define a dictionary containing the username ('testuser') \nand an invalid password ('wrongpassword').\n"
            "   - Send a POST request to the login route ('/login') of the Flask application.\n"
            "   - Include the login form data in the request payload.\n"
        )
        four = (
            "Verify the login outcome:\n"
            "   - Check the response status code:\n"
            "       - If the status code is 401, the login failed due to invalid password.\n"
            "   - Check the response message:\n"
            "       - If the message indicates failure ('Invalid username or password'), the test passes.\n"
            "Expected Outcome:- The test should pass, indicating that the user \nlogin process fails correctly when an invalid password is provided."
        )
        correct_order = [
            one,
            two,
            three,
            four
        ]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        # Add newline character (\n) for multiline text
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
            'Accuracy_Percentage_code_testing_Negative': percentage,
            # Add more fields as needed
        }

        # Data for the nested "times" collection
        time_data = {
            'Time_taken_to_answer_code_testing_Negative': time_taken,
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
        subprocess.Popen(["python", "software_eng_pages/nine_se.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase = Firebase()
    # Retrieve data
    retriveroleid = RetriveRoleId()
    selected_role, user_id = retriveroleid.retrieve_data()
    window = MainWindow(selected_role, user_id, firebase)
    window.mainloop()
    sys.exit(app.exec_())

       
