import random
import math

class Agent:
    def __init__(self, x, y, dx, dy, state = 'S'):
        self.x = x                      # horizontal position
        self.y = y                      # vertical position
        self.dx = dx                    # horizontal movement speed
        self.dy = dy                    # vertical movement speed
        self.state = state              # 'S' (Susceptible), 'I' (Infected), 'R' (Recovered)
        self.infection_timer = 0        # Counts how long the agent has been infected

    def move(self, width, height):
        # Moves the agent, bouncing off walls if hitting canvas boundaries
        self.x += self.dx
        self.y += self.dy

        # Bounce on left/right wall
        if self.x <= 0 or self.x >= width:
            self.dx *= -1
        
        # Boounce on top/bottom wall
        if self.y <= 0 or self.y >= height:
            self.dy *= -1

    def infect(self):
        # Sets the agent's state to infected if they are susceptible
        if self.state == 'S':
            self.state = 'I'
            self.infection_timer = 0

    def recover(self):
         # Sets the agent's state to recovered if they are infected
         if self.state == 'I':
             self.state = 'R'

class SIRSimulation:
    def __init__(self, width, height):
        self.width = width          # Canvas width
        self.height = height        # Canvas height
        self.population = []        # List of Agent objects

        # Simulation parameters (default until set externally)
        self.infection_rate = 0.1
        self.recovery_time = 100
        self.movement_speed = 2
        self.infection_distance = 10
        self.initial_infected = 1
        self.population_size = 100

    def initialize_population(self):
        # Creates a new population of agents with random positions and directions
        self.population.clear()
        for i in range(self.population_size):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            dx = self.movement_speed * math.cos(angle)
            dy = self.movement_speed * math.sin(angle)
            state = 'I' if i < self.initial_infected else 'S'
            self.population.append(Agent(x, y, dx, dy, state))

    def update(self):
        # Runs one step of the simulation: move agents, spead infection, update recovery

        # Move all agents
        for agent in self.population:
            agent.move(self.width, self.height)

        # Spread Infection
        for i, a in enumerate(self.population):
            if a.state != 'I':
                continue
            for j, b in enumerate(self.population):
                if i == j or b.state != 'S':
                    continue
                dist = math.hypot(a.x - b.x, a.y - b.y)
                if dist <= self.infection_distance and random.random() < self.infection_rate:
                    b.infect()

        # Handle recovery
        for agent in self.population:
            if agent.state == 'I':
                agent.infection_timer += 1
                if agent.infection_timer >= self.recovery_time:
                    agent.recover()

    def count_states(self):
        # Returns a tuple of counts: (Susceptible, Infected, Recovered)
        s = sum(1 for a in self.population if a.state == 'S')
        i = sum(1 for a in self.population if a.state == 'I')
        r = sum(1 for a in self.population if a.state == 'R')
        return s, i, r