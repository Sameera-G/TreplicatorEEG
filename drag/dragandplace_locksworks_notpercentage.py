import tkinter as tk
import random

class DraggableCard(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, bg="lightblue", padx=10, pady=5, **kwargs)
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
            self.master.check_order()
            self.snap_to_cage()

    def snap_to_cage(self):
        if not self.locked:
            for cage in self.master.cages:
                if self.winfo_x() > cage[0] and self.winfo_x() < cage[1] and self.winfo_y() > cage[2] and self.winfo_y() < cage[3]:
                    if not cage[4]:  # Check if cage is locked
                        self.place(x=cage[0] + 10, y=cage[2] + 10)
                        self.cage = cage
                        self.master.arrange_cards_in_cage(self)
                    break

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Draggable Cards")
        self.fullScreenState = False
        self.geometry('400x300')
        self.bind("<F11>", self.toggleFullScreen)
        self.bind("<Escape>", self.quitFullScreen)
        self.toggleFullScreen(None)
        self.cards = []
        self.cages = []  # Initialize cages as an empty list
        self.order_label = tk.Label(self, text="Waiting", bg="lightgray")
        self.order_label.place(x=self.winfo_screenwidth() - 100, y=10)
        self.lock_button = tk.Button(self, text="Lock Cages", command=self.lock_cages)
        self.lock_button.place(x=self.winfo_screenwidth() - 100, y=40)
        self.unlock_button = tk.Button(self, text="Unlock Cages", command=self.unlock_cages, state="disabled")
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
        self.lock_button.config(state="disabled")  # Disable lock button
        self.unlock_button.config(state="normal")  # Enable unlock button
        for card in self.cards:
            card.locked = True

    def unlock_cages(self):
        for cage in self.cages:
            cage_list = list(cage)  # Convert tuple to list
            cage_list[4] = False  # Unlock all cages
            self.cages[self.cages.index(cage)] = tuple(cage_list)  # Convert list back to tuple
        self.unlock_button.config(state="disabled")  # Disable unlock button
        self.lock_button.config(state="normal")  # Enable lock button
        for card in self.cards:
            card.locked = False

    def create_cages(self):
        cage_height = int(self.winfo_screenheight() * 0.2)
        cage_width = 100
        num_cages = 4
        for i in range(num_cages):
            cage_y = i * (self.winfo_screenheight() // num_cages)
            cage = (10, 10 + cage_width, cage_y, cage_y + cage_height, False)  # Add lock status to cage tuple
            tk.Canvas(self, width=cage_width, height=cage_height, bg="lightyellow").place(x=10, y=cage_y)
            self.cages.append(cage)

    def create_cards(self):
        card_texts = ["Apple", "Banana", "Orange", "Grape"]
        random.shuffle(card_texts)  # Shuffle the card texts randomly
        num_cards = len(card_texts)
        for i in range(num_cards):
            card_text = card_texts[i]
            card = DraggableCard(self, text=card_text, font=("Arial", 12))
            card.place(x=random.randint(50, 300), y=random.randint(50, 200))  # Randomly place the card
            self.cards.append(card)

    def check_order(self):
        correct_order = ["Apple", "Banana", "Orange", "Grape"]
        total_correct = 0
        total_expected = 0
        for cage in self.cages:
            cards_in_cage = [card.cget("text") for card in self.cards if cage[2] < card.winfo_y() < cage[3]]
            for i, card_text in enumerate(cards_in_cage):
                if i < len(correct_order) and card_text == correct_order[i]:
                    total_correct += 1
                total_expected += 1
        if total_expected == 0:
            self.order_label.config(text="Waiting")
        else:
            percentage_in_order = (total_correct / (len(correct_order) * len(self.cages))) * 100
            self.order_label.config(text=f"Order: {percentage_in_order:.2f}%")
            if total_correct == len(correct_order) * len(self.cages):
                self.lock_cages()  # Lock cages if all cards are in correct places


    def arrange_cards_in_cage(self, card):
        cards_in_cage = [c for c in self.cards if c.cage == card.cage]
        for i, c in enumerate(cards_in_cage):
            c.place(x=card.cage[0] + 10, y=card.cage[2] + 10 + (i * 40))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
