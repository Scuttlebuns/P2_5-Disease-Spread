import os
import tkinter as tk
from datetime import datetime

from simulation import GRID_SIZE, CELL_SIZE, STEP_DELAY, Simulation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GridCanvas(tk.Canvas):
    """Draws the agents on a GRID_SIZE×GRID_SIZE canvas."""
    COLORS = {"S": "blue", "I": "red", "R": "green", "D": "black"}

    def __init__(self, parent, sim):
        size_px = GRID_SIZE * CELL_SIZE
        super().__init__(parent, width=size_px, height=size_px, bg="white")
        self.sim = sim

    def draw(self):
        self.delete("all")
        for ag in self.sim.agents:
            x1, y1 = ag.x * CELL_SIZE, ag.y * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.create_rectangle(x1, y1, x2, y2,
                                  fill=self.COLORS[ag.state],
                                  width=0)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Disease Spread & Social Behavior")
        self.running = False
        self.after_id = None
        self.sim = None
        self.time_step = 0
        self.total_agents = 0

        # ─── Control panel ───
        ctrl = tk.Frame(root, pady=5)
        ctrl.pack(fill="x")

        def make_ctrl(label, var, col, default):
            tk.Label(ctrl, text=label).grid(row=0, column=col, padx=5)
            var.set(default)
            tk.Entry(ctrl, textvariable=var, width=5).grid(row=1, column=col, padx=5)

        self.density_var   = tk.DoubleVar()
        self.init_inf_var  = tk.DoubleVar()
        self.inf_prob_var  = tk.DoubleVar()
        self.rec_time_var  = tk.IntVar()
        self.mort_rate_var = tk.DoubleVar()

        make_ctrl("Density %",      self.density_var,   0, 60)
        make_ctrl("Init Infect %",  self.init_inf_var,  1,  2)
        make_ctrl("Infect Prob %",  self.inf_prob_var,  2, 25)
        make_ctrl("Recovery Time",  self.rec_time_var,  3, 10)
        make_ctrl("Mortality %",    self.mort_rate_var, 4,  2)

        tk.Button(ctrl, text="Start", command=self.start).grid(row=1, column=5, padx=5)
        tk.Button(ctrl, text="Pause", command=self.pause).grid(row=1, column=6, padx=5)
        tk.Button(ctrl, text="Reset", command=self.reset).grid(row=1, column=7, padx=5)

        # ─── Main content ───
        content = tk.Frame(root)
        content.pack(fill="both", expand=True)

        # Left: grid
        left = tk.Frame(content)
        left.pack(side="left", padx=5, pady=5)
        self.canvas = GridCanvas(left, None)
        self.canvas.pack()

        # Right: chart
        right = tk.Frame(content)
        right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.figure = Figure(figsize=(5,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("SIR Model Over Time")
        self.ax.set_xlabel("Time Steps")
        self.ax.set_ylabel("Population")
        self.line_s, = self.ax.plot([], [], color="blue", label="Susceptible")
        self.line_i, = self.ax.plot([], [], color="red",  label="Infected")
        self.line_r, = self.ax.plot([], [], color="green",label="Recovered")
        self.ax.legend()

        self.fig_canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.fig_canvas.get_tk_widget().pack(fill="both", expand=True)

        # ─── Status bar ───
        self.status = tk.Label(root, text="Step: 0 | S: 0 | I: 0 | R: 0 | D: 0")
        self.status.pack(pady=5)

    def start(self):
        if self.running:
            return

        # read & normalize inputs
        density   = max(0.0, min(1.0, self.density_var.get()   / 100))
        init_inf  = max(0.0, min(1.0, self.init_inf_var.get()  / 100))
        inf_prob  = max(0.0, min(1.0, self.inf_prob_var.get()  / 100))
        rec_time  = max(1,     self.rec_time_var.get())
        mort_rate = max(0.0, min(1.0, self.mort_rate_var.get() / 100))

        # init simulation
        self.sim = Simulation(density, init_inf, inf_prob, rec_time, mort_rate)
        self.total_agents = len(self.sim.agents)
        self.time_step = 0
        self.running = True

        # reset chart data
        self.x_data = []
        self.s_data = []
        self.i_data = []
        self.r_data = []

        # draw initial state
        self.canvas.sim = self.sim
        self.canvas.draw()
        self._update_chart()
        self.update_status()
        self._loop()

    def _loop(self):
        if not self.running:
            return

        self.sim.step()
        self.canvas.draw()
        self.time_step += 1

        s, i, r, d = self.sim.counts()
        self.update_status(s, i, r, d)

        # append & redraw chart
        self.x_data.append(self.time_step)
        self.s_data.append(s)
        self.i_data.append(i)
        self.r_data.append(r)
        self._update_chart()

        if i > 0:
            self.after_id = self.root.after(STEP_DELAY, self._loop)
        else:
            self.running = False
            self._show_summary(s, i, r, d)

    def _update_chart(self):
        self.line_s.set_data(self.x_data, self.s_data)
        self.line_i.set_data(self.x_data, self.i_data)
        self.line_r.set_data(self.x_data, self.r_data)
        self.ax.set_xlim(0, max(10, self.time_step))
        self.ax.set_ylim(0, self.total_agents)
        self.fig_canvas.draw()

    def pause(self):
        if getattr(self, "after_id", None):
            self.root.after_cancel(self.after_id)
        self.running = False

    def reset(self):
        self.pause()
        self.time_step = 0
        self.canvas.delete("all")
        self.ax.clear()
        self.ax.set_title("SIR Model Over Time")
        self.ax.set_xlabel("Time Steps")
        self.ax.set_ylabel("Population")
        self.ax.legend(handles=[self.line_s, self.line_i, self.line_r])
        self.fig_canvas.draw()
        self.status.config(text="Step: 0 | S: 0 | I: 0 | R: 0 | D: 0")

    def update_status(self, s=0, i=0, r=0, d=0):
        self.status.config(
            text=f"Step: {self.time_step} | S: {s} | I: {i} | R: {r} | D: {d}"
        )

    def _show_summary(self, s, i, r, d):
        win = tk.Toplevel(self.root)
        win.title("Simulation Complete")
        win.grab_set()

        tk.Label(win, text="The epidemic has ended.", font=("Arial", 14)).pack(pady=(10, 5))

        info = [
            f"Total time steps: {self.time_step}",
            f"Susceptible: {s}",
            f"Infected: {i}",
            f"Recovered: {r}",
            f"Dead: {d}",
        ]
        for line in info:
            tk.Label(win, text=line, anchor="w").pack(fill="x", padx=20)

        tk.Label(win, text="").pack()
        msg = "Congratulations\nThe population survived!" if (s + r) > 0 else "The population did not survive."
        tk.Label(win, text=msg, font=("Arial", 12)).pack(pady=(0, 10))

        # Export Graph button
        def on_export():
            dt = datetime.now().strftime("%Y%m%d_%H%M%S")
            count = 1
            fname = f"{dt}_run{count}_graph.png"
            while os.path.exists(fname):
                count += 1
                fname = f"{dt}_run{count}_graph.png"
            try:
                self.figure.savefig(fname)
                tk.Label(win, text=f"Export successful: {fname}").pack()
            except Exception as e:
                tk.Label(win, text=f"Export failed: {e}").pack()

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Export Graph", command=on_export).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close",        command=win.destroy).pack(side="left", padx=5)