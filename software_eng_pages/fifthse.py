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

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list

        # Load text from file
        self.load_text_from_file("software_eng_pages/paragraphs_se/softeeng_task_description.txt")

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
                canvas.place(x=10, y=self.winfo_screenheight() * 0.05, relwidth=0.2, relheight=0.9)

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
        self.stopwatch_label.place(x=self.winfo_screenwidth() - 100, y=100)
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
        cage_height = int(self.winfo_screenheight() * 0.9 / 3.05)
        num_cages = 5
        left_margin_percentage = 0.22  # 22% space from the left side of the screen

        # Calculate the width of the cages after leaving space on the left
        cage_width = int((self.winfo_screenwidth() * (1 - left_margin_percentage)) / num_cages) * 2
        cage_x_start = int(self.winfo_screenwidth() * left_margin_percentage)  # Starting X position

        top_margin_percentage = 0.05  # 5% space from the top of the screen
        space_between_cages = 2  # Adjust this value as needed

        # Create the first two cages in a row
        for i in range(2):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage)
            cage = (cage_x_start + i * (cage_width + space_between_cages), cage_x_start + (i + 1) * cage_width,
                    cage_y, cage_y + cage_height, False)
            self.create_curved_cage(cage_width, cage_height, cage_x_start + i * (cage_width + space_between_cages), cage_y)
            self.create_cage_number(cage_x_start + (i + 1) * cage_width - 20, cage_y + 10, i + 1)
            self.cages.append(cage)

        # Create the next two cages in the second row
        for i in range(2, 4):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage) + cage_height + space_between_cages
            cage = (cage_x_start + (i - 2) * (cage_width + space_between_cages), cage_x_start + (i - 1) * cage_width,
                    cage_y, cage_y + cage_height, False)
            self.create_curved_cage(cage_width, cage_height, cage_x_start + (i - 2) * (cage_width + space_between_cages), cage_y)
            self.create_cage_number(cage_x_start + (i - 1) * cage_width - 20, cage_y + 10, i + 1)
            self.cages.append(cage)

        # Create the last cage in the third row
        cage_y = int(self.winfo_screenheight() * top_margin_percentage) + 2 * (cage_height + space_between_cages)
        cage = (cage_x_start, cage_x_start + cage_width, cage_y, cage_y + cage_height, False)
        self.create_curved_cage(cage_width, cage_height, cage_x_start, cage_y)
        self.create_cage_number(cage_x_start + cage_width - 20, cage_y + 10, 5)
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
        user_registration = (
            "def function():\n"
            "    form = RegistrationForm(request.form)\n"
            "    if form.validate():\n"
            "        username = form.username.data\n"
            "        email = form.email.data\n"
            "        password = form.password.data\n"
            "        hashed_password = hash_password(password)\n"
            "        return jsonify({\"message\": \"User registered successfully\"})\n"
            "    else:\n"
            "        return jsonify({\"message\": \"Form validation failed\"}), 400\n"
        )
        user_login = (
            "def login():\n"
            "   username = request.json.get('username')\n"
            "   password = request.json.get('password')\n"
            "   if user and check_password_hash(user.password, password):\n"
            "       return jsonify({\"message\": \"Login successful\"})\n"
            "   else:\n"
            "   return jsonify({\"message\": \"Invalid username or password\"}), 401\n"
        )
        password_hashing = (
            "from werkzeug.security import generate_password_hash\n"
            "def hash_password(password):\n"
            "    return generate_password_hash(password)\n"
        )
        form_validation = (
            "from wtforms import Form, StringField, PasswordField, validators\n"
            "class RegistrationForm(Form):\n"
            "    username = StringField('Username', [validators.Length(min=4, max=25)])\n"
            "    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])\n"
            "    password = PasswordField('New Password', [\n"
            "        validators.DataRequired(),\n"
            "        validators.EqualTo('confirm', message='Passwords must match'),\n"
            "        validators.Length(min=8, max=35)])\n"
            "    confirm = PasswordField('Repeat Password')\n"
        )
        session_management = (
            "app.secret_key = 'your_secret_key'\n"
            "@app.route('/login', methods=['POST'])\n"
            "def login():\n"
            "    session['logged_in'] = True\n"
            "    return redirect(url_for('dashboard'))\n"
            "@app.route('/logout')\n"
            "def logout():\n"
            "    session.pop('logged_in', None)\n"
            "    return redirect(url_for('index'))\n"
            "@app.route('/dashboard')\n"
            "def dashboard():\n"
            "    if 'logged_in' in session:\n"
            "        return \"Welcome to the dashboard\"\n"
            "    else:\n"
            "        return redirect(url_for('index'))\n"
        )
        card_texts = [
            user_registration,
            user_login,
            password_hashing,
            form_validation,
            session_management
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
        user_registration = (
            "def function():\n"
            "    form = RegistrationForm(request.form)\n"
            "    if form.validate():\n"
            "        username = form.username.data\n"
            "        email = form.email.data\n"
            "        password = form.password.data\n"
            "        hashed_password = hash_password(password)\n"
            "        return jsonify({\"message\": \"User registered successfully\"})\n"
            "    else:\n"
            "        return jsonify({\"message\": \"Form validation failed\"}), 400\n"
        )
        user_login = (
            "def login():\n"
            "   username = request.json.get('username')\n"
            "   password = request.json.get('password')\n"
            "   if user and check_password_hash(user.password, password):\n"
            "       return jsonify({\"message\": \"Login successful\"})\n"
            "   else:\n"
            "   return jsonify({\"message\": \"Invalid username or password\"}), 401\n"
        )
        password_hashing = (
            "from werkzeug.security import generate_password_hash\n"
            "def hash_password(password):\n"
            "    return generate_password_hash(password)\n"
        )
        form_validation = (
            "from wtforms import Form, StringField, PasswordField, validators\n"
            "class RegistrationForm(Form):\n"
            "    username = StringField('Username', [validators.Length(min=4, max=25)])\n"
            "    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])\n"
            "    password = PasswordField('New Password', [\n"
            "        validators.DataRequired(),\n"
            "        validators.EqualTo('confirm', message='Passwords must match'),\n"
            "        validators.Length(min=8, max=35)])\n"
            "    confirm = PasswordField('Repeat Password')\n"
        )
        session_management = (
            "app.secret_key = 'your_secret_key'\n"
            "@app.route('/login', methods=['POST'])\n"
            "def login():\n"
            "    session['logged_in'] = True\n"
            "    return redirect(url_for('dashboard'))\n"
            "@app.route('/logout')\n"
            "def logout():\n"
            "    session.pop('logged_in', None)\n"
            "    return redirect(url_for('index'))\n"
            "@app.route('/dashboard')\n"
            "def dashboard():\n"
            "    if 'logged_in' in session:\n"
            "        return \"Welcome to the dashboard\"\n"
            "    else:\n"
            "        return redirect(url_for('index'))\n"
        )
        correct_order = [
            user_registration,
            user_login,
            password_hashing,
            form_validation,
            session_management
        ]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = 5 #len(self.cards)
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
        data = {
            'Accuracy_Percentage_development_coding': percentage,
            'Time_taken_to_answer_development_coding': time_taken,
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
    window = MainWindow()
    window.mainloop()
    sys.exit(app.exec_())

       
