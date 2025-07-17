# simulation.py
import random

# Constants
GRID_SIZE = 50    # cells per side
CELL_SIZE = 10    # pixels per cell
STEP_DELAY = 100  # ms between steps

class Agent:
    """
    Represents one individual on the grid.
    state: "S"/"I"/"R"/"D"
    timer: counts steps since infection
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "S"
        self.timer = 0

class Simulation:
    """
    Grid-based SIR+D simulation.
    """
    def __init__(self, density, init_inf_pct, inf_prob, rec_time, mort_rate):
        self.density        = density
        self.init_inf_pct   = init_inf_pct
        self.inf_prob       = inf_prob
        self.rec_time       = rec_time
        self.mort_rate      = mort_rate
        self.agents         = []
        self.reset()

    def reset(self):
        """(Re)initialize agents on the grid."""
        all_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        n_agents = int(len(all_cells) * self.density)
        chosen   = random.sample(all_cells, n_agents)
        self.agents = [Agent(x, y) for x, y in chosen]

        # infect initial subset
        n_init = max(1, int(n_agents * self.init_inf_pct))
        for ag in random.sample(self.agents, n_init):
            ag.state = "I"
            ag.timer = 0

    def step(self):
        # 1) move (dead agents stay put)
        for ag in self.agents:
            if ag.state == "D":
                continue
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            ag.x = max(0, min(GRID_SIZE - 1, ag.x + dx))
            ag.y = max(0, min(GRID_SIZE - 1, ag.y + dy))

        # 2) infection pass
        for ag in self.agents:
            if ag.state != "S":
                continue
            for other in self.agents:
                if (other.state == "I" and
                    abs(ag.x - other.x) <= 1 and
                    abs(ag.y - other.y) <= 1):
                    if random.random() < self.inf_prob:
                        ag.state = "I"
                        ag.timer = 0
                    break

        # 3) recovery or death
        for ag in self.agents:
            if ag.state == "I":
                ag.timer += 1
                if ag.timer >= self.rec_time:
                    if random.random() < self.mort_rate:
                        ag.state = "D"
                    else:
                        ag.state = "R"

    def counts(self):
        """Return counts of S, I, R, D agents."""
        s = sum(a.state == "S" for a in self.agents)
        i = sum(a.state == "I" for a in self.agents)
        r = sum(a.state == "R" for a in self.agents)
        d = sum(a.state == "D" for a in self.agents)
        return s, i, r, d
