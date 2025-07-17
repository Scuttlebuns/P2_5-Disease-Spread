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
    compliance: whether they obey distancing
    recovery_duration: # steps until recovery/death
    """
    def __init__(self, x, y, compliance=True):
        self.x = x
        self.y = y
        self.state = "S"
        self.timer = 0
        self.compliance = compliance
        self.recovery_duration = None

class Simulation:
    """
    Grid-based SIR+D with distancing & compliance,
    recovery times and non-compliance drawn from normals.
    """
    def __init__(
        self,
        density,
        init_inf_pct,
        inf_prob,
        rec_time,
        mort_rate,
        cdc_threshold_pct,
        non_compliance_pct
    ):
        self.density            = density
        self.init_inf_pct       = init_inf_pct
        self.inf_prob           = inf_prob
        self.rec_time_mean      = rec_time
        self.rec_time_sigma     = rec_time / 4.0
        self.mort_rate          = mort_rate
        self.cdc_threshold_pct  = cdc_threshold_pct
        self.nc_mean            = non_compliance_pct
        self.nc_sigma           = non_compliance_pct / 4.0

        self.agents = []
        self.total_infections = 0
        self.distancing_active = False
        self.reset()

    def reset(self):
        """(Re)initialize agents, infection count, distancing flag."""
        self.total_infections = 0
        self.distancing_active = False

        # sample non-compliance fraction from N(mean, sigma)
        nc = random.gauss(self.nc_mean, self.nc_sigma)
        nc = max(0.0, min(1.0, nc))

        all_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        n_agents = int(len(all_cells) * self.density)
        chosen   = random.sample(all_cells, n_agents)

        self.agents = [
            Agent(x, y, compliance=(random.random() > nc))
            for x, y in chosen
        ]

        # infect initial subset and assign recovery durations
        n_init = max(1, int(n_agents * self.init_inf_pct))
        for ag in random.sample(self.agents, n_init):
            ag.state = "I"
            ag.timer = 0
            ag.recovery_duration = max(
                1,
                int(round(random.gauss(self.rec_time_mean, self.rec_time_sigma)))
            )
            self.total_infections += 1

    def _neighbors(self, x, y):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    yield nx, ny

    def step(self):
        # activate distancing if threshold reached
        if (self.total_infections / len(self.agents)) >= self.cdc_threshold_pct:
            self.distancing_active = True

        # occupancy map of alive agents
        occ = {(ag.x, ag.y): ag for ag in self.agents if ag.state != "D"}

        # 1) move
        for ag in self.agents:
            if ag.state == "D":
                continue

            moves = list(self._neighbors(ag.x, ag.y))
            random.shuffle(moves)
            moved = False

            for nx, ny in moves:
                if (nx, ny) in occ:
                    continue
                if self.distancing_active and ag.compliance:
                    # ensure no neighbors at new spot
                    if any((mx, my) in occ for mx, my in self._neighbors(nx, ny)):
                        continue

                del occ[(ag.x, ag.y)]
                ag.x, ag.y = nx, ny
                occ[(nx, ny)] = ag
                moved = True
                break

            if not moved:
                for nx, ny in moves:
                    if (nx, ny) not in occ:
                        del occ[(ag.x, ag.y)]
                        ag.x, ag.y = nx, ny
                        occ[(nx, ny)] = ag
                        break

        # 2) infection
        for ag in self.agents:
            if ag.state != "S":
                continue
            for nx, ny in self._neighbors(ag.x, ag.y):
                other = occ.get((nx, ny))
                if other and other.state == "I":
                    if random.random() < self.inf_prob:
                        ag.state = "I"
                        ag.timer = 0
                        ag.recovery_duration = max(
                            1,
                            int(round(random.gauss(self.rec_time_mean, self.rec_time_sigma)))
                        )
                        self.total_infections += 1
                    break

        # 3) recovery or death
        for ag in self.agents:
            if ag.state == "I":
                ag.timer += 1
                if ag.timer >= ag.recovery_duration:
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