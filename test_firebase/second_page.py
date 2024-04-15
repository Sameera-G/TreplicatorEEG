import tkinter as tk
from tkinter import ttk
from firebase_class import Firebase

class SecondPage(tk.Frame):
    def __init__(self, master=None, firebase=None, user_id=None):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.firebase = firebase  # Accept firebase instance as a parameter
        self.create_widgets()

    def create_widgets(self):
        self.percentage_label = ttk.Label(self, text="Percentage:")
        self.percentage_entry = ttk.Entry(self)
        self.time_label = ttk.Label(self, text="Time:")
        self.time_entry = ttk.Entry(self)
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_data)

        self.percentage_label.grid(row=0, column=0, sticky=tk.W)
        self.percentage_entry.grid(row=0, column=1)
        self.time_label.grid(row=1, column=0, sticky=tk.W)
        self.time_entry.grid(row=1, column=1)
        self.submit_button.grid(row=2, columnspan=2)
        
        self.grid(row=0, column=0, padx=10, pady=10)  # Add this line to actually place the frame in the root window

    def submit_data(self):
        percentage = self.percentage_entry.get()
        time = self.time_entry.get()
        self.firebase.update_data(self.user_id, {"percentage": percentage, "time": time})

def main(user_id):
    root = tk.Tk()
    app = SecondPage(master=root, user_id=user_id)
    app.mainloop()

if __name__ == "__main__":
    user_id = input("Enter User ID: ")
    main(user_id)
