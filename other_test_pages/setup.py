from cx_Freeze import Freezer
from cx_Freeze import setup, Executable

setup(
    name="Treplicator",
    version="1.0",
    description="Description of your application",
    executables=[Executable("mainpage.py")],  # Replace "your_main_script.py" with your main Python script
)
