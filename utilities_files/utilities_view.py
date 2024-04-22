import platform
import tkinter as tk
from ctypes import windll, c_int

# Functions for managing full-screen mode
def toggle_full_screen(window):
    """
    Toggle full-screen mode for a Tkinter window.
    
    Args:
        window (tk.Toplevel or tk.Tk): The window to toggle.
    """
    # Toggle the full-screen attribute
    window.fullScreenState = not window.fullScreenState
    window.attributes("-fullscreen", window.fullScreenState)


def quit_full_screen(window):
    """
    Exit full-screen mode for a Tkinter window.
    
    Args:
        window (tk.Toplevel or tk.Tk): The window to exit from full-screen mode.
    """
    window.fullScreenState = False
    window.attributes("-fullscreen", window.fullScreenState)


# Function to set transparency on Windows
def set_transparency(window_id):
    """
    Set transparency for a window based on its platform.
    
    Args:
        window_id (int): The window ID to set transparency for.
    """
    if platform.system() == "Windows":
        # Enable transparency attribute on Windows
        windll.dwmapi.DwmSetWindowAttribute(window_id, 2, c_int(1), 4)


# Function to create a curved "cage" with platform-specific transparency handling
def create_curved_cage(parent, width, height, x, y):
    """
    Create a Tkinter canvas with specified dimensions and platform-specific transparency.
    
    Args:
        parent (tk.Widget): The parent widget for the canvas.
        width, height (int): Dimensions of the canvas.
        x, y (int): Coordinates to place the canvas.
    
    Returns:
        tk.Canvas: The created canvas with platform-specific adjustments.
    """
    # Create a canvas with specified dimensions and background color
    canvas = tk.Canvas(parent, width=width, height=height, bg="#333333")
    canvas.place(x=x, y=y)

    # Get the window ID for setting transparency
    window_id = canvas.winfo_id()

    # Set platform-specific transparency
    set_transparency(window_id)

    return canvas

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

        return canvas

def create_curved_rectangle(canvas, x1, y1, x2, y2, r):
        canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline="", fill="#1f1f1f")
        canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1 + r, y1, x2 - r, y2, outline="", fill="#1f1f1f")
        canvas.create_rectangle(x1, y1 + r, x2, y2 - r, outline="", fill="#1f1f1f")

#load text file
def load_text_from_file(self, file_path, margin_from_top, relwidth):
        try:
            with open(file_path, "r") as file:
                content = file.read()

                # Create a canvas for curved corners
                canvas = tk.Canvas(self, bg="#1f1f1f", highlightbackground=None, highlightthickness=0)
                canvas.place(x=10, y=self.winfo_screenheight() * margin_from_top, relwidth=relwidth, relheight=0.9)

                # Add curved corners to the canvas
                create_curved_rectangle(canvas, 0, 0, canvas.winfo_width(), canvas.winfo_height(), 50)

                # Create the text widget
                text_widget = tk.Text(canvas, wrap="word", bg="#1f1f1f", fg="white", font=("Arial", 12),
                                    highlightbackground="#1f1f1f", highlightthickness=5, padx=10, pady=10)
                text_widget.insert("1.0", content)
                text_widget.place(relwidth=1, relheight=1)
                text_widget.config(state="disabled")  # Make the text area read-only
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

#Create cages thirdpage
def create_cages(self, num_cages, top_margin_percentage, bottom_margin_percentage, left_margin_percentage):
        cage_height = int(self.winfo_screenheight() * (1 - top_margin_percentage - bottom_margin_percentage)/5 * 0.9)
        # Calculate the width of the cages after leaving space on the left
        cage_width = int((self.winfo_screenwidth() * (1 - left_margin_percentage)) / num_cages) * 2
        cage_x_start = int(self.winfo_screenwidth() * left_margin_percentage)  # Starting X position

        available_height = self.winfo_screenheight() * (1 - top_margin_percentage - bottom_margin_percentage)

        for i in range(num_cages):
            cage_y = int(self.winfo_screenheight() * top_margin_percentage) + (i * (cage_height + (5 + available_height - (cage_height * num_cages)) / (num_cages - 1)))
            cage = (cage_x_start, cage_x_start + cage_width, cage_y, cage_y + cage_height, False)  # Add lock status to cage tuple
            self.create_curved_cage(cage_width, cage_height, cage_x_start, cage_y)
            self.cages.append(cage)


"""def calculate_percentage(self, correct_order):
        total_correct = 0
        total_cards = 5 #len(correct_order)
        for i, cage in enumerate(self.cages):
            cards_in_cage = [
                card for card in self.cards if cage[2] < card.winfo_y() < cage[3]
            ]
            if len(cards_in_cage) == 1:
                card_text = cards_in_cage[0].cget("text")
                if card_text == correct_order[i]:
                    total_correct += 1
        percentage = (total_correct / total_cards) * 100 if total_cards != 0 else 0
        self.order_label.config(text=f"Accuracy: {percentage:.2f}%", fg="white")
        return percentage"""


