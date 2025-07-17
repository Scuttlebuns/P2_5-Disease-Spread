# interface.py
import tkinter as tk
from simulation import GRID_SIZE, CELL_SIZE, STEP_DELAY, Simulation

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
            x1 = ag.x * CELL_SIZE
            y1 = ag.y * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
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

        # ─── Control panel ───
        ctrl = tk.Frame(root, pady=5)
        ctrl.pack()

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

        # ─── Grid canvas ───
        self.canvas = GridCanvas(root, None)
        self.canvas.pack(expand=True)

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
        self.time_step = 0
        self.running = True
        self.canvas.sim = self.sim
        self.canvas.draw()
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

        if i > 0:
            self.after_id = self.root.after(STEP_DELAY, self._loop)
        else:
            self.running = False
            # determine survival based on any survivors
            msg = (
                "Congratulations\nThe population survived!"
                if (s + r) > 0
                else "The population did not survive."
            )
            self._show_summary(s, i, r, d, msg)

    def pause(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False

    def reset(self):
        self.pause()
        self.time_step = 0
        self.canvas.delete("all")
        self.status.config(text="Step: 0 | S: 0 | I: 0 | R: 0 | D: 0")

    def update_status(self, s=0, i=0, r=0, d=0):
        self.status.config(
            text=f"Step: {self.time_step} | S: {s} | I: {i} | R: {r} | D: {d}"
        )

    def _show_summary(self, s, i, r, d, msg):
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
        tk.Label(win, text=msg, font=("Arial", 12)).pack(pady=(0, 10))

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Export Graph", command=self._export_graph).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=win.destroy).pack(side="left", padx=5)

    def _export_graph(self):
        print("Exporting graph…")