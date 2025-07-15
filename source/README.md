# P1_6-Infection

SIR Disease Spread Simulation

How does a disease spread through a population—and what factors determine whether an outbreak dies out or infects
everyone? This simulation models an epidemic using the classic SIR (Susceptible-Infected-Recovered) framework,
where each individual is represented as a moving dot. Blue dots are susceptible (healthy, but can be infected), red
dots are currently infected (and able to spread the disease), and green dots are recovered (immune and no longer
able to transmit the infection). The simulation provides an interactive, visual way to explore the mathematics behind
epidemics and public health.

At each step, all agents move randomly around the simulation area, occasionally bouncing off the walls. When an
infected agent gets close enough to a susceptible one, there is a chance (set by the infection rate) that the susceptible
agent will become infected as well. Infected agents will eventually recover after a set number of time steps (the
recovery time), turning green and becoming permanently immune to further infection. The interplay between
movement, chance encounters, infection probability, and recovery determines the overall course of the
epidemic—sometimes leading to rapid outbreaks, sometimes to quick containment.

SIR models like this one are fundamental in epidemiology and public health planning, helping scientists and
decision-makers understand how changes in disease properties or social behavior affect the spread of illness. By
letting students visualize and manipulate these factors directly, the simulation offers an accessible introduction to the
science of disease modeling—and highlights the unpredictable, emergent nature of real-world epidemics.

How to Use the Simulation

Set the population size, initial number of infected individuals, infection rate (chance of transmission on contact),
recovery time (how long someone remains infectious), and movement speed using the controls at the top. Press
"Start" to watch the outbreak unfold. The main canvas shows agents moving and changing color as their state
changes, while the graph on the right tracks the number of susceptible, infected, and recovered individuals over time.
You can pause or reset the simulation at any time to try new scenarios. Experiment with different values to see how
faster movement, higher infection rates, or longer recovery periods affect the spread—and how interventions might
slow or stop an epidemic!

Background

The SIR model is a fundamental approach in epidemiology for understanding disease outbreaks. It classifies
individuals as:
    ● S (Susceptible): Not yet infected, but can catch the disease.
    ● I (Infected): Currently infected and can spread the disease.
    ● R (Recovered): No longer infected and immune.
Agent-based models simulate each person as an individual, making the process more realistic and visually intuitive.

Simulation Rules

1. Agents:
    ○ Each individual is represented by a moving dot.
    ○ States: Susceptible (blue), Infected (red), Recovered (green).
2. Disease Spread:
    ○ Each time step, infected agents can infect any susceptible agents within a certain distance, with
      probability set by the infection rate.
    ○ Infected agents recover after a user-set recovery time and then become permanently immune.
3. Agent Movement:
    ○ All agents move randomly within the simulation area, bouncing off the edges.
4. Simulation Controls:
    ○ User sets population size, initial infected count, infection rate, recovery time, and movement speed.
    ○ Controls to start, pause, and reset the simulation.
5. Visualization:
    ○ The simulation shows agents moving and changing color as their state changes.
    ○ A live-updating plot displays the number of susceptible, infected, and recovered individuals over time.
    ○ On-screen statistics show counts and time.

Assignment Tasks

1. Run the Simulation:
    ○ Set up and run at least three different scenarios by changing infection rate, recovery time, movement
      speed, and initial infected count.
    ○ Observe and record what happens in each case.
2. Data Collection:
    ○ For each scenario, track and save:
        ■ Number of susceptible, infected, and recovered over time (from the plot).
        ■ Total duration of outbreak.
        ■ Any notable patterns (e.g., rapid outbreaks, slow spreads, or no outbreak).
3. Analysis and Visualization:
    ○ Produce clear plots for each scenario.
    ○ Discuss:
        ■ How changing infection rate or recovery time changes the outbreak’s spread.
        ■ What factors help limit or accelerate the epidemic.
        ■ Whether the outbreak always infects everyone, or can "burn out" before that happens.
4. Report Requirements (2–4 pages)
    ● Submit:
    ○ Your simulation code.
    ○ Screenshots (or video) showing the simulation in progress.
    ○ A brief written report (1–2 pages) following the guidelines in the first lecture slides.
A seven-minute presentation of your findings, with three minutes afterward for questions and answers.
