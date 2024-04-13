import tkinter as tk

class DraggableCard(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, bg="lightblue", padx=10, pady=5, **kwargs)
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        
    def on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag_motion(self, event):
        x = self.winfo_x() - self._drag_start_x + event.x
        y = self.winfo_y() - self._drag_start_y + event.y
        self.place(x=x, y=y)

def main():
    root = tk.Tk()
    root.title("Draggable Cards")
    root.geometry("400x400")

    card1 = DraggableCard(root, text="Card 1")
    card1.place(x=50, y=50)

    card2 = DraggableCard(root, text="Card 2")
    card2.place(x=200, y=50)

    root.mainloop()

if __name__ == "__main__":
    main()
