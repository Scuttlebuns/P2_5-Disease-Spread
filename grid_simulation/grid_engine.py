# grid_simulation/grid_engine.py

import random

class Agent:
    def __init__(self, x, y, status="S", immune_level=0.0, compliant=True):
        self.x = x
        self.y = y
        self.status = status  # "S", "I", "R", "D"
        self.immune_level = immune_level
        self.compliant = compliant
        self.infection_timer = 0

class GridEngine:
    def __init__(self, grid_size=50, population_density=0.6):
        self.grid_size = grid_size
        self.population_density = population_density
        self.agents = []
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.time_step = 0
        self.reset()

    def reset(self):
        self.time_step = 0
        self.agents.clear()
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if random.random() < self.population_density:
                    compliant = random.random() > 0.15
                    agent = Agent(i, j, status="S", compliant=compliant)
                    self.agents.append(agent)
                    self.grid[i][j] = agent

        # Infect a few individuals initially
        initial_infected = max(1, int(0.02 * len(self.agents)))
        infected_agents = random.sample(self.agents, initial_infected)
        for agent in infected_agents:
            agent.status = "I"

    def step(self):
        self.time_step += 1
        new_infections = []

        for agent in self.agents:
            if agent.status != "D":
                self.move_agent(agent)

        for agent in self.agents:
            if agent.status == "I":
                neighbors = self.get_neighbors(agent.x, agent.y)
                for neighbor in neighbors:
                    if neighbor.status == "S" and random.random() < 0.2:
                        new_infections.append(neighbor)

                agent.infection_timer += 1
                if agent.infection_timer >= 10:
                    if random.random() < 0.02:
                        agent.status = "D"
                    else:
                        agent.status = "R"
                        agent.immune_level = min(1.0, random.gauss(0.7, 0.1))

        for agent in new_infections:
            agent.status = "I"
            agent.infection_timer = 0

    def move_agent(self, agent):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        new_x = (agent.x + dx) % self.grid_size
        new_y = (agent.y + dy) % self.grid_size

        if self.grid[new_x][new_y] is None:
            self.grid[agent.x][agent.y] = None
            agent.x = new_x
            agent.y = new_y
            self.grid[new_x][new_y] = agent

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.grid_size
                ny = (y + dy) % self.grid_size
                neighbor = self.grid[nx][ny]
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors

    def stats(self):
        s = sum(1 for a in self.agents if a.status == "S")
        i = sum(1 for a in self.agents if a.status == "I")
        r = sum(1 for a in self.agents if a.status == "R")
        d = sum(1 for a in self.agents if a.status == "D")
        return {"S": s, "I": i, "R": r, "D": d}