import sys
import tkinter as tk
import time
from PIL import Image, ImageTk
import subprocess
sys.path.append('I:/Research/TreplicatorEEG/utilities_files')
from stop_watch import StopWatch
from firebase_func import Firebase
from retrive_role_id import RetriveRoleId
from utilities_view import toggle_full_screen, quit_full_screen, load_text_from_file


class TrueFalseButton(tk.Button):
    def __init__(self, master, text, on_click_callback):
        super().__init__(master, text=text, font=("Arial", 12))
        self.state = "unchecked"
        self.on_click_callback = on_click_callback
        self.config(bg="#d3d3d3", command=self.change_state)

    def change_state(self):
        if self.state == "unchecked":
            self.config(text="Correct", bg="#33cc33")
            self.state = "True"
        elif self.state == "True":
            self.config(text="Wrong", bg="#ff3333")
            self.state = "False"
        else:
            self.config(text="Unchecked", bg="#d3d3d3")
            self.state = "unchecked"
        
        # Call the callback function with the new state
        if self.on_click_callback:
            self.on_click_callback(self.state)

        return self.state


class StopWatch:
    def __init__(self):
        self.start_time = time.time()

    @property
    def elapsed_seconds(self):
        return round(time.time() - self.start_time)


class MainWindow(tk.Tk):
    def __init__(self, selected_role, user_id, firebase):
        super().__init__()
        self.title("True/False Assessment")
        self.geometry("800x600")
        self.selected_role = selected_role
        self.user_id = user_id
        self.firebase = firebase
        self.fullScreenState = False
        self.bind("<F11>", self.toggleFullScreen)
        self.bind("<Escape>", self.quitFullScreen)
        self.toggleFullScreen()

        # Keep track of TrueFalseButton states
        self.button_references = []

        self.questions = [
            {"text": "Nuclear physics is a branch of chemistry that studies the nucleus of the atom.", "correct_answer": "False", "given_answer": "False"},
            {"text": "The nucleus of an atom is made up of protons and electrons.", "correct_answer": "False", "given_answer": "True"},
            {"text": "Nuclear physics played no role in the development of radiation therapy for cancer.", "correct_answer": "False", "given_answer": "False"},
            {"text": "The strong nuclear force is effective over long distances within the nucleus.", "correct_answer": "False", "given_answer": "False"},
            {"text": "Quantum mechanics is not necessary for understanding the behavior of the nucleus.", "correct_answer": "False", "given_answer": "False"},
            {"text": "Nuclear fission is the process by which two nuclei combine to form a heavier nucleus.", "correct_answer": "False", "given_answer": "False"},
            {"text": "The discovery of the nucleus was made possible by the work of Albert Einstein.", "correct_answer": "False", "given_answer": "False"},
            {"text": "Nuclear power plants use the process of nuclear fusion to generate electricity.", "correct_answer": "False", "given_answer": "False"},
        ]

        # Background setup
        self.background_image = Image.open("images/background1.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title ribbon with headline title text box
        title_frame = tk.Frame(self, bg="black", bd=0, highlightthickness=0)
        title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        title_label = tk.Label(
            title_frame,
            text="True/False Assessment - Select Correct Answers",
            fg="white",
            bg="black",
            font=("Arial", 16, "bold"),
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # Create question frame with black background and white font color for questions
        question_frame = tk.Frame(self, bg='#333333')
        question_frame.place(relx=0.37, rely=0.07, relwidth=0.52, relheight=0.7)

        wrap_length = int(0.40 * (self.winfo_screenwidth()))
        for index, question in enumerate(self.questions):
            # Extract the given_answer with a default value
            given_answer = question.get("given_answer", "Unchecked")
            
            # Text to display in the label
            question_text = f"{question['text']} \nAnswer: {given_answer}"
            question_label = tk.Label(
                question_frame,
                text=question_text,
                font=("Arial", 12),
                fg="white",
                border=10,
                bg="#333333",
                justify="left",
                wraplength=wrap_length,
            )
            question_label.grid(row=index, column=0, sticky="w", padx=(10, 0), pady=(0, 0))

            button = TrueFalseButton(
                question_frame,
                "Unchecked",
                on_click_callback=lambda state, i=index: self.update_button_reference(state, i),
            )
            button.grid(row=index, column=1, sticky="e", padx=(10, 0))

        # Text box to display the percentage
        self.percentage_text = tk.Text(
            self, height=1, width=15, font=("Arial", 16), bg="#333333", fg="white"
        )
        self.percentage_text.place(relx=0.94, rely=0.84, anchor="se",)

        # "Next Page" button
        self.next_button = tk.Button(
            self, text="Next Page", font=("Arial", 16), command=self.goToNextPage, bg="#333333", fg="white",
        )
        self.next_button.place(
            relx=0.94, rely=0.94, anchor="se",
        )

        self.stopwatch = StopWatch()
        self.stopwatch_label = tk.Label(
            self, text=str(self.stopwatch.elapsed_seconds), font=("Arial", 20), bg="black", fg="white"
        )

        #load text to read
        self.load_text_from_file("paragraphs/teacher_curriculum_description.txt", 0.07, 0.35)

        self.stopwatch_label.place(relx=0.95, rely=0.07, anchor="ne")

        self.update_stopwatch()  # Start the stopwatch loop

    def update_stopwatch(self):
        # Update the stopwatch label with the current elapsed time
        self.stopwatch_label.config(text=f"{self.stopwatch.elapsed_seconds}")

        # Schedule this method to run again in 1 second
        self.after(1000, self.update_stopwatch)

    def update_button_reference(self, state, index):
        if index < len(self.button_references):
            self.button_references[index] = state
        else:
            self.button_references.append(state)

    def create_questions(self):
        question_frame = tk.Frame(self, bg='#333333')
        question_frame.place(relx=0.37, rely=0.07, relwidth=0.5, relheight=0.7)
        wrap_length = int(0.40 * (self.winfo_screenwidth()))

        for index, question in enumerate(self.questions):
            # Extract the given_answer with a default value
            given_answer = question.get("given_answer", "Unchecked")
            
            # Text to display in the label
            question_text = f"{question['text']} Answer: {given_answer}"
            
            question_label = tk.Label(
                question_frame,
                text=question_text,
                font=("Arial", 12),
                fg="white",
                border=10,
                bg="#333333",
                justify="right",
                wraplength=wrap_length,
            )
            question_label.grid(row=index, column=0, sticky="w", padx=(10, 0), pady=(10, 0))

            # Create button with callback function
            button = TrueFalseButton(
                question_frame,
                "Unchecked",
                on_click_callback=lambda state, index=index: self.update_button_reference(state, index),
            )
            button.grid(row=index, column=1, sticky="e", padx=(10, 0))

        # Initialize references with default state
        self.update_button_reference("unchecked", index)

    def calculate_percentage(self):
        total_questions = len(self.questions)
        # Ensure the list of button references is at least as long as the number of questions
        while len(self.button_references) < total_questions:
            self.button_references.append("unchecked")  # Default value
        correct_answers = sum(
            1 for i in range(total_questions)
            # Correct answer given and the button was clicked as True
            if (self.questions[i]["correct_answer"] == self.questions[i]["given_answer"] and self.button_references[i] == "True")
            # Incorrect answer given but the button was clicked as False
            or (self.questions[i]["correct_answer"] != self.questions[i]["given_answer"] and self.button_references[i] == "False")
            if self.button_references[i] != "unchecked"
        )

        percentage = (correct_answers / total_questions) * 100
        return percentage

    def goToNextPage(self):

        given_ans = []
        for question in self.questions:
            # Using the correct key and avoiding KeyError by defaulting to "unchecked"
            given_ans.append(question.get("given_answer", "Unchecked"))
        print(given_ans)
        #print(str(self.questions["correct_answers"]))
        print(self.button_references)

        # Calculate percentage
        percentage = self.calculate_percentage()
        # Update stopwatch and get the time taken
        time_taken = self.update_stopwatch()
        # Example usage: Adding data to Firestore

        main_data = {
            'Accuracy_Percentage_user_story': percentage,
            # Add more fields as needed
        }

        # Data for the nested "times" collection
        time_data = {
            'Time_taken_to_answer_user_story': time_taken,
        }
        # Update the main collection (selected_role/user_id)
        firebase.update_data(self.selected_role, self.user_id, main_data)
        # Add to the nested "times" collection using the new method
        firebase.add_time_data(self.selected_role, self.user_id, time_data)

        self.percentage_text.delete("1.0", "end")  # Clear any existing text
        self.percentage_text.insert("1.0", f"Accuracy: {percentage:.2f}%")

        subprocess.Popen(["python", "teacher_pages/retrive_t.py"])

    def toggleFullScreen(self):
        toggle_full_screen(self)

    def quitFullScreen(self):
        quit_full_screen(self)

    def load_text_from_file(self, file_path, margin_from_top, relwidth):
        load_text_from_file(self, file_path, margin_from_top, relwidth)


if __name__ == "__main__":
    firebase = Firebase()
    # Retrieve data
    retriveroleid = RetriveRoleId()
    selected_role, user_id = retriveroleid.retrieve_data()
    window = MainWindow(selected_role, user_id, firebase)
    window.mainloop()
