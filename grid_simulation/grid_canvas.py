# grid_simulation/grid_canvas.py

import tkinter as tk

class GridCanvas(tk.Canvas):
    def __init__(self, parent, engine, cell_size=10, *args, **kwargs):
        self.engine = engine
        self.cell_size = cell_size
        width = engine.grid_size * cell_size
        height = engine.grid_size * cell_size
        super().__init__(parent, width=width, height=height, *args, **kwargs)

    def draw(self):
        self.delete("all")
        for agent in self.engine.agents:
            color = "blue"
            if agent.status == "I":
                color = "red"
            elif agent.status == "R":
                color = "green"
            elif agent.status == "D":
                color = "black"

            x1 = agent.x * self.cell_size
            y1 = agent.y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")