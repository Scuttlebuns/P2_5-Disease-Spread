# Project 2  
## Disease Spread and Social Behavior

### Objective
Use a grid-based agent simulation to model the spread of an infectious disease through a population. Evaluate how factors such as immunity, behavior, mortality, and public health guidelines affect the outcome of an outbreak. Simulate scenarios with varying compliance and analyze their effects on infection peaks, fatality rates, and long-term immunity.

### Background
Infectious diseases spread through interactions between individuals, and outcomes depend heavily on a mix of biological and social factors. Modeling disease spread helps public health officials make decisions about distancing guidelines, vaccination policies, and lockdowns.

In this project, you will simulate a population distributed on a 2D grid. Individuals move, interact, and transmit disease based on proximity and behavior rules. You will analyze the effects of compliance with CDC recommendations, natural immunity, and mortality risk on the spread and severity of an outbreak.

This project includes:
- Dynamic population movement on a grid
- Infection, recovery, and death modeling
- Social behavior simulation (distancing and disobedience)
- Variable immunity modeled with probability distributions
- Scenario experimentation and epidemic analysis

### 85 / 15 Rule
Following the instructions laid out here is 85% of the assignment. You must add something significant to the project. In other words, if you did everything in these instructions perfectly but nothing else, the highest grade you can receive for the project is 85%.

---

### Simulation Rules
- **Grid Size:** 50×50 or larger  
- **Initial Infected Individuals:** Randomly selected small percentage (e.g., 1–3%)  
- **States:** Susceptible, Infected, Recovered (immune), Dead

Each individual follows these rules:
- Moves randomly in one of 8 directions each time step
- Can become infected if an infected person is in one of the 8 cells around them
- Has a chance of dying while infected (mortality rate)
- If they recover, gain partial immunity drawn from a normal distribution ∼N(0.7, 0.1)
- After X% infections, the CDC will demand agents not enter cells when another agent would be next to them
- Y% of agents will ignore that requirement

---

### Adjustable Variables
- Population density (initial percentage of grid cells containing an agent)
- Infection probability on contact
- Number of infections before CDC distancing protocols start
- Recovery time (e.g., 5–14 steps) based on a normal distribution
- Mortality rate (e.g., 1–10%)
- Percent of population that ignores distancing guidelines (e.g., 10–30%) based on a normal distribution

---

### Implementation
Build a discrete-time simulation with individuals as agents on a 2D grid.  
Each agent has properties:
- Position
- Infection status
- Immune level
- Compliance flag

At each time step:
- Agents move (respecting or violating distance rules)
- Infection is evaluated between nearby individuals
- Infected agents either recover (with immunity) or die after a fixed or random time
- Track infection history, status changes, and population-level statistics

---

### Base Case Analysis
Run a simulation with the following base scenario:
- **Grid:** 50×50  
- **Population density:** 60%  
- **Initial infection rate:** 2%  
- **Mortality rate:** 2%  
- **Recovery time:** 10 time steps  
- **15% non-compliance with distancing**

Answer the following:
- What was the peak number of infected individuals?
- What percentage of the population died?
- How long did the outbreak last?
- What was the average immunity level post-outbreak?

---

### Policy Experiments
#### A. Distancing Compliance Variants
- Increase non-compliance to 25%  
- Increase non-compliance to 40%

Compare outbreak intensity and fatality to base case.  
Analyze: Does reduced distancing lead to significantly higher infection rates or deaths?

#### B. Immunity Variability
- Change post-recovery immunity distribution to N(0.5, 0.2)  
- Fixed 100% immunity

Analyze: How does immunity level affect the chance of a second outbreak?

---

### Reporting
Your final report should include:
- Assumptions made (movement logic, infection model, etc.)
- Simulation code
- Plots showing infection, recovery, and death counts over time
- Grid snapshots or animations of disease spread
- A written report (2–3 pages) discussing:
  - Model behavior
  - Parameter effects
  - Policy implications

---

### Submission Requirements
- Python/Java/other simulation code
- Screenshots or video (optional but encouraged)
- Written report (2–3 pages)
- Oral presentation (7 minutes + 3 minutes Q&A)
