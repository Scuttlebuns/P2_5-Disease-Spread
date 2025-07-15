import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import datetime

# matplotlib.use("Agg")

class SIRGraph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a figure and axis
        self.fig, self.ax = plt.subplots(figsize = (5, 3.5), dpi = 100, constrained_layout = True)
        #self.fig.tight_layout()
        self.ax.set_title("SIR Model Over Time", fontsize = 10)
        self.ax.set_xlabel("Time Steps", fontsize = 9)
        self.ax.set_ylabel("Population", fontsize = 9)
        self.ax.tick_params(labelsize = 8)
        self.ax.grid(True)

        # Dummy time axis and initial lines
        self.x_data = []
        self.s_data = []
        self.i_data = []
        self.r_data = []

        self.s_line = self.ax.plot([], [], label = "Susceptible", color = "blue")[0]
        self.i_line = self.ax.plot([], [], label = "Infected",    color = "red")[0]
        self.r_line = self.ax.plot([], [], label = "Recovered",   color = "green")[0]

        self.ax.legend()

        # Embed in tkinter frame
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)
        self.canvas.draw()

    def add_points(self, time_step, s, i, r):
        self.x_data.append(time_step)
        self.s_data.append(s)
        self.i_data.append(i)
        self.r_data.append(r)

        self.s_line.set_data(self.x_data, self.s_data)
        self.i_line.set_data(self.x_data, self.i_data)
        self.r_line.set_data(self.x_data, self.r_data)

        self.ax.set_xlim(0, max(100, time_step))
        self.ax.set_ylim(0, max(self.s_data + self.i_data + self.r_data) + 10)

        self.canvas.draw()

    def export(self, filename = "sir_graph.png"):
        # Attempt to export
        try:
            self.fig.savefig(filename, dpi = 300)
            print(f"Graph saved as: {filename}")
        except Exception as e:
            print(f"error: {e}")
            
    def clear(self):
        self.x_data.clear()
        self.s_data.clear()
        self.i_data.clear()
        self.r_data.clear()

        self.s_line.set_data([], [])
        self.i_line.set_data([], [])
        self.r_line.set_data([], [])
        self.canvas.draw()