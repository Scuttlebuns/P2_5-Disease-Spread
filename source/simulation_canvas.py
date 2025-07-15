# GUI Tool Kit
import tkinter as tk

# Define custom class that inherits tk.canvas
class SimulationCanvas(tk.Canvas):
    # Intitializes a blank white 400x700 canvas
    def __init__(self, parent):
        super().__init__(parent, bg = "white", highlightthickness = 0)
        
        