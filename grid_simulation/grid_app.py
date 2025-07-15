from tkinter import Tk, Frame
from grid_simulation.grid_engine import GridEngine
from grid_simulation.grid_canvas import GridCanvas
from source.controls import create_controls
from source.graph import SIRGraph

class GridApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Disease Spread Grid Simulation")

        self.engine = GridEngine(grid_size=50, population_density=0.6)

        # Controls
        self.controls_frame, self.params, self.start_btn, self.pause_btn, self.reset_btn = create_controls(self.root)
        self.controls_frame.grid(row=0, column=0, sticky="ew")

        # Simulation and graph layout
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=1, column=0)

        self.simulation_canvas = GridCanvas(self.main_frame, self.engine)
        self.simulation_canvas.grid(row=0, column=0)

        self.graph = SIRGraph(self.main_frame)
        self.graph.grid(row=0, column=1)

        self.running = False

        self.start_btn.config(command=self.start_simulation)
        self.pause_btn.config(command=self.pause_simulation)
        self.reset_btn.config(command=self.reset_simulation)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.update_simulation()

    def pause_simulation(self):
        self.running = False

    def reset_simulation(self):
        self.running = False
        self.engine.reset()
        self.simulation_canvas.draw()
        self.graph.clear()

    def update_simulation(self):
        if self.running:
            self.engine.step()
            self.simulation_canvas.draw()
            stats = self.engine.stats()
            self.graph.add_points(self.engine.time_step, stats["S"], stats["I"], stats["R"])
            self.root.after(100, self.update_simulation)

    def run(self):
        self.root.mainloop()