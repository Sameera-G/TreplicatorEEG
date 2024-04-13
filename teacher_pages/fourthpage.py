import sys
import tkinter as tk
import random
from PIL import Image, ImageTk
import platform
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
sys.path.append('I:/Research/treplicator3')
from stop_watch import StopWatch

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

    def goBack(self):
        self.hide()  # Just hide instead of closing, so it can be shown again
        if self.parent:
            self.parent.show()  # Show the TaskReplicatorApp window again

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

        layout = QVBoxLayout()

        # Back button
        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.goBack)
        self.backButton.setFont(QFont('Arial', 12))
        self.backButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        layout.addWidget(self.backButton, alignment=Qt.AlignLeft)

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list

        # Load text from file
        self.load_text_from_file("paragraphs/weekly_breakdown.txt")  # Replace 'your_text_file.txt' with your file path

        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 10))
        self.order_label.place(x=self.winfo_screenwidth() - 150, y=self.winfo_screenheight() - 100)
        self.lock_button = tk.Button(self, text="Next Page", command=self.lock_cages, font=("Arial", 10), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - 150, y=self.winfo_screenheight() - 140)
        #self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        #self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()

        # Create stopwatch
        self.stopwatch_label = tk.Label(self, text="", bg="#1f1f1f", fg="white", font=("Arial", 16))
        self.stopwatch_label.place(x=self.winfo_screenwidth() - 100, y=80)
        # Create stopwatch instance
        self.stopwatch = StopWatch()
        # Update stopwatch label every second
        self.update_stopwatch()

    def update_stopwatch(self):
        self.stopwatch_label.config(text=self.stopwatch.elapsedTime)
        self.after(1000, self.update_stopwatch)

    def goBack(self):
        self.hide()  # Just hide instead of closing, so it can be shown again
        if self.parent:
            self.parent.show()  # Show the TaskReplicatorApp window again

    def load_text_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()

                # Create a canvas for curved corners
                canvas = tk.Canvas(self, bg="#1f1f1f", highlightbackground="#1f1f1f", highlightthickness=0)
                canvas.place(x=10, y=self.winfo_screenheight() * 0.05, relwidth=0.25, relheight=0.9)

                # Add curved corners to the canvas
                self.create_curved_rectangle(canvas, 0, 0, canvas.winfo_width(), canvas.winfo_height(), 50)

                # Create the text widget
                text_widget = tk.Text(canvas, wrap="word", bg="#1f1f1f", fg="white", font=("Arial", 12),
                                    highlightbackground="#1f1f1f", highlightthickness=5, padx=10, pady=10)
                text_widget.insert("1.0", content)
                text_widget.place(relwidth=1, relheight=1)
                text_widget.config(state="disabled")  # Make the text area read-only
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

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
        cage_height = int(self.winfo_screenheight() * 0.9/7 * 0.9)
        num_cages = 7
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
            kcgnullwindow_id = 0
            kcg_windowlist_option_all = 0
            kcgwindow_image_option_default = 0

            # Define necessary structures and types
            class CGRect(Structure):
                _fields_ = [("origin", c_void_p), ("size", c_void_p)]

            #cgf_loat = c_float
            #cf_index = c_int

            # Get necessary functions from CoreGraphics framework
            #cg_window_list_copy_window_info = windll.CoreGraphics.cg_window_list_copy_window_info
            cgwindow_list_create_image = windll.CoreGraphics.cgwindow_list_create_image
            cgwindow_list_create_image.restype = c_void_p
            cgwindow_list_create_image.argtypes = [CGRect, c_int, c_int, c_int]

            # Set transparency by calling macOS-specific functions
            image = cgwindow_list_create_image(CGRect(), kcg_windowlist_option_all, kcgnullwindow_id, kcgwindow_image_option_default)
            canvas.create_image(0, 0, image=image, anchor=tk.NW)

        elif platform.system() == "Linux":
            # Set transparency for Linux using the window ID
            # Note: Linux transparency might require additional configuration
            pass


    def create_cards(self):
        card_texts = [
            "Introduction to Atomic Structure and the Discovery of the Nucleus \n(Overview of atomic theory and the Rutherford gold foil experiment) \n(Components of the nucleus: protons, neutrons, and nuclear forces)",
            "Forces Within the Nucleus \n(The Strong Nuclear Force and its comparison to electromagnetic and gravitational forces) \n(Quantum mechanics introduction relevant to nuclear bonding)",
            "Models of Nuclear Structure \n(The Liquid Drop Model: concept, applications, and limitations) \n(The Shell Model: understanding shell structure in nuclei)",
            "Radioactivity and Nuclear Reactions \n(Types of radioactivity and decay processes) \n(Nuclear fission: principles, chain reactions, and reactors)",
            "Nuclear Fusion and Energy Production \n(The process of nuclear fusion in stars and experimental reactors) \n(Comparison of fission and fusion as energy sources, including challenges and advancements)",
            "Applications of Nuclear Physics \n(Nuclear physics in medicine - radiation therapy and diagnostic imaging) \n(Industrial and environmental applications - material analysis, dating techniques, and nuclear waste management)",
            "Ethical and Societal Impact \n(The role of nuclear energy in addressing climate change) \n(Nuclear non-proliferation, waste management, and ethical considerations)",
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
            "Introduction to Atomic Structure and the Discovery of the Nucleus \n(Overview of atomic theory and the Rutherford gold foil experiment) \n(Components of the nucleus: protons, neutrons, and nuclear forces)",
            "Forces Within the Nucleus \n(The Strong Nuclear Force and its comparison to electromagnetic and gravitational forces) \n(Quantum mechanics introduction relevant to nuclear bonding)",
            "Models of Nuclear Structure \n(The Liquid Drop Model: concept, applications, and limitations) \n(The Shell Model: understanding shell structure in nuclei)",
            "Radioactivity and Nuclear Reactions \n(Types of radioactivity and decay processes) \n(Nuclear fission: principles, chain reactions, and reactors)",
            "Nuclear Fusion and Energy Production \n(The process of nuclear fusion in stars and experimental reactors) \n(Comparison of fission and fusion as energy sources, including challenges and advancements)",
            "Applications of Nuclear Physics \n(Nuclear physics in medicine - radiation therapy and diagnostic imaging) \n(Industrial and environmental applications - material analysis, dating techniques, and nuclear waste management)",
            "Ethical and Societal Impact \n(The role of nuclear energy in addressing climate change) \n(Nuclear non-proliferation, waste management, and ethical considerations)",
        ]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        # Add newline character (\n) for multiline text
        self.order_label.config(text=f"Order: {percentage:.2f}%", fg="white")


    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.mainloop()
    sys.exit(app.exec_())

       
