import tkinter as tk
import random

# ─────────────── Constants ───────────────
GRID_SIZE  = 50   # 50×50 cells
CELL_SIZE  = 10   # pixels per cell
STEP_DELAY = 100  # ms between simulation steps
# ──────────────────────────────────────────

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "S"  # S, I, R or D
        self.timer = 0    # counts steps since infection

class Simulation:
    def __init__(self, density, init_inf_pct, inf_prob, rec_time, mort_rate):
        self.density        = density
        self.init_inf_pct   = init_inf_pct
        self.inf_prob       = inf_prob
        self.rec_time       = rec_time
        self.mort_rate      = mort_rate
        self.agents         = []
        self.reset()

    def reset(self):
        # place agents randomly
        all_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        n_agents = int(len(all_cells) * self.density)
        chosen  = random.sample(all_cells, n_agents)
        self.agents = [Agent(x,y) for x,y in chosen]

        # infect initial subset
        n_init = max(1, int(n_agents * self.init_inf_pct))
        for ag in random.sample(self.agents, n_init):
            ag.state = "I"
            ag.timer = 0

    def step(self):
        # 1) move
        for ag in self.agents:
            if ag.state == "D":
                continue
            dx, dy = random.choice([-1,0,1]), random.choice([-1,0,1])
            ag.x = max(0, min(GRID_SIZE-1, ag.x + dx))
            ag.y = max(0, min(GRID_SIZE-1, ag.y + dy))

        # 2) infect neighbors
        for ag in self.agents:
            if ag.state != "S":
                continue
            for other in self.agents:
                if other.state=="I" and abs(ag.x-other.x)<=1 and abs(ag.y-other.y)<=1:
                    if random.random() < self.inf_prob:
                        ag.state = "I"
                        ag.timer = 0
                    break

        # 3) recover or die
        for ag in self.agents:
            if ag.state=="I":
                ag.timer += 1
                if ag.timer >= self.rec_time:
                    if random.random() < self.mort_rate:
                        ag.state = "D"
                    else:
                        ag.state = "R"

    def counts(self):
        s = sum(a.state=="S" for a in self.agents)
        i = sum(a.state=="I" for a in self.agents)
        r = sum(a.state=="R" for a in self.agents)
        d = sum(a.state=="D" for a in self.agents)
        return s, i, r, d

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
            ent = tk.Entry(ctrl, textvariable=var, width=5)
            ent.grid(row=1, column=col, padx=5)

        self.density_var     = tk.DoubleVar()
        self.init_inf_var    = tk.DoubleVar()
        self.inf_prob_var    = tk.DoubleVar()
        self.rec_time_var    = tk.IntVar()
        self.mort_rate_var   = tk.DoubleVar()

        make_ctrl("Density %",     self.density_var,  0, 60)
        make_ctrl("Init Infected %",self.init_inf_var, 1,  2)
        make_ctrl("Infect Prob %",  self.inf_prob_var, 2, 25)
        make_ctrl("Recovery Time",  self.rec_time_var, 3, 10)
        make_ctrl("Mortality %",    self.mort_rate_var,4,  2)

        tk.Button(ctrl, text="Start", command=self.start).grid(row=1, column=5, padx=5)
        tk.Button(ctrl, text="Pause", command=self.pause).grid(row=1, column=6, padx=5)
        tk.Button(ctrl, text="Reset", command=self.reset).grid(row=1, column=7, padx=5)

        # ─── Grid Canvas ───
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(expand=True)
        self.canvas = tk.Canvas(
            canvas_frame,
            width=GRID_SIZE*CELL_SIZE,
            height=GRID_SIZE*CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        # ─── Status Bar ───
        self.status = tk.Label(root, text="Step: 0 | S: 0 | I: 0 | R: 0 | D: 0")
        self.status.pack(pady=5)

    def start(self):
        if self.running:
            return
        # read & normalize parameters
        density   = max(0.0, min(1.0, self.density_var.get()/100))
        init_inf  = max(0.0, min(1.0, self.init_inf_var.get()/100))
        inf_prob  = max(0.0, min(1.0, self.inf_prob_var.get()/100))
        rec_time  = max(1,     self.rec_time_var.get())
        mort_rate = max(0.0, min(1.0, self.mort_rate_var.get()/100))

        # new simulation
        self.sim = Simulation(density, init_inf, inf_prob, rec_time, mort_rate)
        self.time_step = 0
        self.running = True
        self.canvas.delete("all")
        self.update_status()
        self._loop()

    def _loop(self):
        if not self.running:
            return
        self.sim.step()
        self.draw()
        self.time_step += 1
        s,i,r,d = self.sim.counts()
        self.update_status(s,i,r,d)
        if i>0:
            self.after_id = self.root.after(STEP_DELAY, self._loop)
        else:
            self.running = False

    def pause(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False

    def reset(self):
        self.pause()
        self.canvas.delete("all")
        self.time_step = 0
        self.status.config(text="Step: 0 | S: 0 | I: 0 | R: 0 | D: 0")

    def draw(self):
        self.canvas.delete("all")
        for ag in self.sim.agents:
            x1 = ag.x * CELL_SIZE
            y1 = ag.y * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = {
                "S":"blue","I":"red","R":"green","D":"black"
            }[ag.state]
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, width=0)

    def update_status(self, s=0, i=0, r=0, d=0):
        self.status.config(
            text=f"Step: {self.time_step} | S: {s} | I: {i} | R: {r} | D: {d}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

