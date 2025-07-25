import os
import tkinter as tk
from datetime import datetime
from simulation import GRID_SIZE, CELL_SIZE, STEP_DELAY, Simulation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Frank stuff
from data_logger import init_log, log_step, save_log  # Place at top of file


class GridCanvas(tk.Canvas):
    # Handles drawing agents to grid with colors by state
    COLORS = {"S": "blue", "I": "red", "R": "green", "D": "black"}

    def __init__(self, parent, sim):
        size_px = GRID_SIZE * CELL_SIZE
        super().__init__(parent, width=size_px, height=size_px, bg="white")
        self.sim = sim

    def draw(self):
        self.delete("all")
        if not self.sim:
            return
        for ag in self.sim.agents:
            x1, y1 = ag.x * CELL_SIZE, ag.y * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.create_rectangle(x1, y1, x2, y2, fill=self.COLORS[ag.state], width=0)

class App:
    # Main GUI + logic
    def __init__(self, root):
        self.root = root
        self.root.title("Disease Spread & Social Behavior")
        self.running = False
        self.after_id = None
        self.sim = None
        self.time_step = 0
        self.total_agents = 0

        # Controls
        ctrl = tk.Frame(root, pady=5)
        ctrl.pack(fill="x")

        def make_ctrl(label, var, col, default):
            tk.Label(ctrl, text=label).grid(row=0, column=col, padx=5)
            var.set(default)
            tk.Entry(ctrl, textvariable=var, width=5).grid(row=1, column=col, padx=5)

        # input for simulation config
        self.density_var        = tk.DoubleVar()
        self.init_inf_var       = tk.DoubleVar()
        self.inf_prob_var       = tk.DoubleVar()
        self.rec_time_var       = tk.IntVar()
        self.mort_rate_var      = tk.DoubleVar()
        self.cdc_threshold_var  = tk.DoubleVar()
        self.non_compliance_var = tk.DoubleVar()

        make_ctrl("Density %",            self.density_var,        0, 60)
        make_ctrl("Init Infect %",        self.init_inf_var,       1,  2)
        make_ctrl("Infect Prob %",        self.inf_prob_var,       2, 25)
        make_ctrl("Recovery Time (mean)", self.rec_time_var,       3, 10)
        make_ctrl("Mortality %",          self.mort_rate_var,      4,  2)
        make_ctrl("Distancing @ % Inf.",  self.cdc_threshold_var,  5, 15)
        make_ctrl("Non-Compliance %",     self.non_compliance_var, 6, 15)

        # control buttons
        tk.Button(ctrl, text="Start", command=self.start).grid(row=1, column=7, padx=5)
        tk.Button(ctrl, text="Pause", command=self.pause).grid(row=1, column=8, padx=5)
        tk.Button(ctrl, text="Reset", command=self.reset).grid(row=1, column=9, padx=5)

        # Layout
        content = tk.Frame(root)
        content.pack(fill="both", expand=True)

        # grid visualization on left
        left = tk.Frame(content)
        left.pack(side="left", padx=5, pady=5)
        self.canvas = GridCanvas(left, None)
        self.canvas.pack()

        # chart on right
        right = tk.Frame(content)
        right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("SIR Model Over Time")
        self.ax.set_xlabel("Time Steps")
        self.ax.set_ylabel("Percent of Population")
        self.ax.set_ylim(0, 100)
        self.line_s, = self.ax.plot([], [], color="blue", label="Susceptible")
        self.line_i, = self.ax.plot([], [], color="red", label="Infected")
        self.line_r, = self.ax.plot([], [], color="green", label="Recovered")
        self.ax.legend()

        self.fig_canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.fig_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Status Bar
        self.status = tk.Label(root, text="Step: 0 | S: 0% | I: 0% | R: 0% | D: 0%")
        self.status.pack(pady=5)

    def start(self):
        # Start simulation from user inputs
        density        = max(0, min(1, self.density_var.get()/100))
        init_inf       = max(0, min(1, self.init_inf_var.get()/100))
        inf_prob       = max(0, min(1, self.inf_prob_var.get()/100))
        rec_time       = max(1, self.rec_time_var.get())
        mort_rate      = max(0, min(1, self.mort_rate_var.get()/100))
        cdc_thresh     = max(0, min(1, self.cdc_threshold_var.get()/100))
        non_compl      = max(0, min(1, self.non_compliance_var.get()/100))

        self.sim = Simulation(density, init_inf, inf_prob, rec_time, mort_rate, cdc_thresh, non_compl)
        init_log()      # Initialize data logger
        self.total_agents = len(self.sim.agents)
        self.time_step = 0
        self.running = True

        self.x_data = []
        self.s_pct = []
        self.i_pct = []
        self.r_pct = []

        self.canvas.sim = self.sim
        self.canvas.draw()
        self._update_chart()
        s, i, r, d = self.sim.counts()
        self.update_status(s, i, r, d)
        self._loop()

    def _loop(self):
        # Continues running simulation until no infected left
        if not self.running:
            return

        self.sim.step()
        self.canvas.draw()
        self.time_step += 1
        s, i, r, d = self.sim.counts()

        log_step(self.time_step, s, i, r, d)        # Log step

        # record chart data
        sp = s / self.total_agents * 100
        ip = i / self.total_agents * 100
        rp = r / self.total_agents * 100
        self.x_data.append(self.time_step)
        self.s_pct.append(sp)
        self.i_pct.append(ip)
        self.r_pct.append(rp)

        self._update_chart()
        self.update_status(s, i, r, d)

        if i > 0:
            self.after_id = self.root.after(STEP_DELAY, self._loop)
        else:
            self.running = False
            self._show_summary(s, i, r, d)

    def _update_chart(self):
        # update chart lines
        self.line_s.set_data(self.x_data, self.s_pct)
        self.line_i.set_data(self.x_data, self.i_pct)
        self.line_r.set_data(self.x_data, self.r_pct)
        self.ax.set_xlim(0, max(10, self.time_step))
        self.fig_canvas.draw()

    def pause(self):
        # stop animation loop
        if getattr(self, "after_id", None):
            self.root.after_cancel(self.after_id)
        self.running = False

    def reset(self):
        # wipe everything: grid, chart, and labels
        self.pause()
        self.time_step = 0
        self.canvas.delete("all")
        self.x_data = []
        self.s_pct = []
        self.i_pct = []
        self.r_pct = []
        self.line_s.set_data([], [])
        self.line_i.set_data([], [])
        self.line_r.set_data([], [])
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        self.fig_canvas.draw()
        self.status.config(text="Step: 0 | S: 0% | I: 0% | R: 0% | D: 0%")

    def update_status(self, s, i, r, d):
        # refresh bottom status bar
        self.status.config(
            text=f"Step: {self.time_step} | S: {s/self.total_agents*100:.1f}% | I: {i/self.total_agents*100:.1f}% | R: {r/self.total_agents*100:.1f}% | D: {d/self.total_agents*100:.1f}%"
        )

    def _show_summary(self, s, i, r, d):
        # simulation complete popup window
        win = tk.Toplevel(self.root)
        win.title("Simulation Complete")
        win.grab_set()

        tk.Label(win, text="The epidemic has ended.", font=("Arial", 14)).pack(pady=(10, 5))

        info = [
            f"Total steps: {self.time_step}",
            f"Susceptible: {s / self.total_agents * 100:.1f}%",
            f"Infected: {i / self.total_agents * 100:.1f}%",
            f"Recovered: {r / self.total_agents * 100:.1f}%",
            f"Dead: {d / self.total_agents * 100:.1f}%"
        ]
        for line in info:
            tk.Label(win, text=line, anchor="w").pack(fill="x", padx=20)

        alive_pct = (s + r) / self.total_agents * 100
        msg = "Population survived." if alive_pct > 50 else "Population did not survive."
        msg += "\n 'Threshold for survival is 50%'"
        tk.Label(win, text=msg, font=("Arial", 12)).pack(pady=(0, 10))

        def on_export():
            dt = datetime.now().strftime("%Y%m%d_%H%M%S")
            count = 1
            fname = f"{dt}_run{count}_chart.png"
            while os.path.exists(fname):
                count += 1
                fname = f"{dt}_run{count}_chart.png"
            try:
                self.figure.savefig(fname)
                tk.Label(win, text=f"Export successful: {fname}").pack()
            except Exception as e:
                tk.Label(win, text=f"Export failed: {e}").pack()

        # export/close buttons
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Export Graph", command=on_export).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=win.destroy).pack(side="left", padx=5)

        save_log(scenario_label = "Rapid_Spread_10")        # Saves log file, change title per scenario