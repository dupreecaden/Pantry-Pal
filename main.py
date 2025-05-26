import tkinter as tk
from Gui import PantryApp
from Pantry import load

if __name__ == "__main__":
    load()
    root = tk.Tk()
    app = PantryApp(root)
    root.mainloop()



