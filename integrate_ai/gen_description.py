import tkinter as tk
import random
from PIL import Image, ImageTk
import platform

class DraggableCard(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, padx=10, pady=5, font=("Arial", 12), **kwargs)
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

        # Configure other widgets as before
        self.configure(bg="#1f1f1f")  # Set background color
        self.cards = []
        self.cages = []  # Initialize cages as an empty list
        self.order_label = tk.Label(self, text="Waiting", bg="#1f1f1f", fg="white", font=("Arial", 10))
        self.order_label.place(x=self.winfo_screenwidth() - 100, y=10)
        self.lock_button = tk.Button(self, text="Lock Cages", command=self.lock_cages, font=("Arial", 10), bg="#333333", fg="white")
        self.lock_button.place(x=self.winfo_screenwidth() - 100, y=40)
        self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled", font=("Arial", 10), bg="#333333", fg="white")
        self.unlock_button.place(x=self.winfo_screenwidth() - 100, y=70)
        self.create_cages()
        self.create_cards()

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
        cage_height = int(self.winfo_screenheight() * 0.1)
        cage_width = 400
        num_cages = 5
        for i in range(num_cages):
            cage_y = i * (self.winfo_screenheight() // num_cages)
            cage = (10, 10 + cage_width, cage_y, cage_y + cage_height, False)  # Add lock status to cage tuple
            self.create_curved_cage(cage_width, cage_height, cage_y)
            self.cages.append(cage)

    def create_curved_cage(self, width, height, y):
        canvas = tk.Canvas(self, width=width, height=height, bg="#333333")
        canvas.place(x=10, y=y)

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
            kCGWindowAlpha = 5
            kCGNullWindowID = 0
            kCGWindowListOptionAll = 0
            kCGWindowImageOptionDefault = 0

            # Define necessary structures and types
            class CGRect(Structure):
                _fields_ = [("origin", c_void_p), ("size", c_void_p)]

            CGFloat = c_float
            CFIndex = c_int

            # Get necessary functions from CoreGraphics framework
            CGWindowListCopyWindowInfo = windll.CoreGraphics.CGWindowListCopyWindowInfo
            CGWindowListCreateImage = windll.CoreGraphics.CGWindowListCreateImage
            CGWindowListCreateImage.restype = c_void_p
            CGWindowListCreateImage.argtypes = [CGRect, c_int, c_int, c_int]

            # Set transparency by calling macOS-specific functions
            image = CGWindowListCreateImage(CGRect(), kCGWindowListOptionAll, kCGNullWindowID, kCGWindowImageOptionDefault)
            canvas.create_image(0, 0, image=image, anchor=tk.NW)

        elif platform.system() == "Linux":
            # Set transparency for Linux using the window ID
            # Note: Linux transparency might require additional configuration
            pass

    def create_cards(self):
        card_texts = ["Apple", "Banana", "Orange", "Grape", "guvava"]
        random.shuffle(card_texts)
        num_cards = len(card_texts)
        right_margin = 20  # Set the margin from the right side of the screen
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self, text=card_text, bg="#4c4c4c", fg="white")
            # Place the card on the right-hand side with a margin
            card.place(x=self.winfo_screenwidth() - right_margin - card.winfo_reqwidth() * 5,
                    y=random.randint(90, 400))  
            self.cards.append(card)

    def calculate_percentage(self):
        correct_order = ["Apple", "Banana", "Orange", "Grape", "guvava"]
        total_correct = sum(1 for cage in self.cages for card in self.cards
                            if cage[2] < card.winfo_y() < cage[3] and card.cget("text") == correct_order[self.cages.index(cage)])
        total_cards = len(self.cards)
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        self.order_label.config(text=f"Order: {percentage:.2f}%", fg="white")

    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()