import tkinter as tk
from tkinter import ttk
from firebase_class import Firebase
from PIL import Image, ImageTk
import random
import platform
import sys
sys.path.append('I:/Research/TreplicatorEEG/utilities_files')
from stop_watch import StopWatch
from firebase import Firebase

class SecondPage(tk.Frame):
    def __init__(self, master=None, user_id=None):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.firebase = Firebase()  # Initialize Firebase
        self.create_widgets()
        self.create_main_window()

    def create_widgets(self):
        # Create widgets for data submission
        self.percentage_label = ttk.Label(self, text="Percentage:")
        self.percentage_entry = ttk.Entry(self)
        self.time_label = ttk.Label(self, text="Time:")
        self.time_entry = ttk.Entry(self)
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_data)

        # Place widgets in grid layout
        self.percentage_label.grid(row=0, column=0, sticky=tk.W)
        self.percentage_entry.grid(row=0, column=1)
        self.time_label.grid(row=1, column=0, sticky=tk.W)
        self.time_entry.grid(row=1, column=1)
        self.submit_button.grid(row=2, columnspan=2)

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

    def create_main_window(self):
        # Create the main window with background image and other components
        self.master.title("Draggable Cards")
        self.master.geometry('400x300')
        self.master.configure(bg="#1f1f1f")

        # Load background image
        self.background_image = Image.open("images/background1.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create other components
        self.order_label = tk.Label(self.master, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 20))
        self.order_label.place(x=self.master.winfo_screenwidth() - self.master.winfo_screenwidth() * 0.2, y=self.master.winfo_screenheight() * 0.7)
        self.lock_button = tk.Button(self.master, text="Next Page", command=self.lock_cages, font=("Arial", 20), bg="#333333", fg="white")
        self.lock_button.place(x=self.master.winfo_screenwidth() - self.master.winfo_screenwidth() * 0.2, y=self.master.winfo_screenheight() * 0.8)

        # Create stopwatch
        self.stopwatch_label = tk.Label(self.master, text="", bg="#1f1f1f", fg="white", font=("Arial", 16))
        self.stopwatch_label.place(x=self.master.winfo_screenwidth() - 100, y=100)
        # Create stopwatch instance
        self.stopwatch = StopWatch()
        # Update stopwatch label every second
        self.update_stopwatch()

        # Create draggable cards
        self.cards = []
        self.create_cards()

    def submit_data(self):
        percentage = self.percentage_entry.get()
        time = self.time_entry.get()
        self.firebase.update_data(self.user_id, {"percentage": percentage, "time": time})

    def lock_cages(self):
        # Implement the locking functionality
        pass

    def calculate_percentage(self):
        correct_order = [
            "As a user, I want to create a new account on the educational \nweb application so that I can access \nexclusive features and content.",
            "As a user, I want to log in to my existing account using my \nemail address and password to access \npersonalized content and track my progress.",
            "As a user, I want the ability to reset my password if I forget it, \nensuring that I can regain access to my account securely.",
            "As an administrator, I want to manage user accounts, including \nactivating, deactivating, and deleting accounts as needed.",
            "As a developer, I want to implement user authentication \nsecurely, protecting user data and credentials \nfrom unauthorized access.",
            "As a developer, I want the user to change \nthe operators profile picture"
        ]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        # Add newline character (\n) for multiline text
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")
        return percentage

    def create_cards(self):
        # Create draggable cards
        card_texts = [
            "As a user, I want to create a new account on the educational \nweb application so that I can access \nexclusive features and content.",
            "As a user, I want to log in to my existing account using my \nemail address and password to access \npersonalized content and track my progress.",
            "As a user, I want the ability to reset my password if I forget it, \nensuring that I can regain access to my account securely.",
            "As an administrator, I want to manage user accounts, including \nactivating, deactivating, and deleting accounts as needed.",
            "As a developer, I want to implement user authentication \nsecurely, protecting user data and credentials \nfrom unauthorized access.",
            "As a developer, I want the user to change \nthe operators profile picture"
        ]
        random.shuffle(card_texts)
        num_cards = len(card_texts)
        right_margin = 20  # Set the margin from the right side of the screen
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self.master, text=card_text, bg="#4c4c4c", fg="white", font=("Arial", 10))
            # Place the card on the right-hand side with a margin
            card.place(
                x=self.master.winfo_screenwidth() - right_margin - card.winfo_reqwidth() * 1,
                y=random.randint(90, 400)
            )
            self.cards.append(card)

    def update_stopwatch(self):
        self.stopwatch_label.config(text=self.stopwatch.elapsedTime)
        self.after(1000, self.update_stopwatch)
        return self.stopwatch.elapsedTime

class StopWatch:
    def __init__(self):
        self.elapsedTime = "00:00:00"

# Draggable card class
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

def main(user_id):
    root = tk.Tk()
    app = SecondPage(master=root, user_id=user_id)
    app.mainloop()

if __name__ == "__main__":
    user_id = input("Enter User ID: ")
    main(user_id)
