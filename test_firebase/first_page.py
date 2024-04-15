import tkinter as tk
from tkinter import ttk
from firebase_class import Firebase
from second_page import SecondPage  # Import the SecondPage class

class FirstPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.firebase = Firebase()
        self.create_widgets()

    def create_widgets(self):
        self.user_id_label = ttk.Label(self, text="User ID:")
        self.user_id_entry = ttk.Entry(self)
        self.hardness_label = ttk.Label(self, text="Hardness:")
        self.hardness_entry = ttk.Entry(self)
        self.submit_button = ttk.Button(self, text="Submit", command=self.open_second_page)

        self.user_id_label.grid(row=0, column=0, sticky=tk.W)
        self.user_id_entry.grid(row=0, column=1)
        self.hardness_label.grid(row=1, column=0, sticky=tk.W)
        self.hardness_entry.grid(row=1, column=1)
        self.submit_button.grid(row=2, columnspan=2)
        
        self.grid(row=0, column=0, padx=10, pady=10)  # Add this line to actually place the frame in the root window

    def open_second_page(self):
        user_id = self.user_id_entry.get()
        hardness = self.hardness_entry.get()
        self.firebase.add_data(user_id, {"hardness": hardness})
        self.master.destroy()  # Close the first page
        SecondPage(master=tk.Tk(), firebase=self.firebase, user_id=user_id)  # Pass Firebase instance

def main():
    root = tk.Tk()
    app = FirstPage(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
