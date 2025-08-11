# Disease Spread and Social Behavior Simulation

## Overview
This project uses a grid-based agent simulation to model the spread of an infectious disease through a population. It explores how factors such as immunity, behavior, mortality, and public health guidelines can influence the course of an outbreak. The simulation allows experimentation with varying compliance levels and analyzes their effects on infection peaks, fatality rates, and long-term immunity.

## Background
Infectious diseases spread through interactions between individuals, and outcomes depend on a mix of biological and social factors. Modeling disease spread can provide valuable insights into how distancing guidelines, vaccination, and behavioral differences shape an epidemic.

This simulation models a population distributed on a 2D grid where individuals move, interact, and transmit disease based on proximity and behavior rules. It includes variables for compliance with health recommendations, natural immunity, and mortality risk.

Key features:
- Dynamic population movement on a grid
- Infection, recovery, and death modeling
- Social behavior simulation (distancing and disobedience)
- Variable immunity modeled with probability distributions
- Scenario experimentation and epidemic analysis

---


### Installation Steps
1. **Create and activate a virtual environment:**
```bash
# create the environment
python3 -m venv venv
```
2. **Activate the environment**
```bash
source venv/bin/activate # macOS/Linux  
venv\\Scripts\\activate # Windows
```
3. **Install requirements.txt**
```bash
pip install -r requirements.txt
```

4. **Run the program**
```bash
python3 main.py
```

---

### Simulation Rules
- **Grid Size:** 50×50  
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
A discrete-time simulation with individuals as agents on a 2D grid.  
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
Some of the scenarios ran:
- **Grid:** 50×50  
- **Population density:** 60%  
- **Initial infection rate:** 2%  
- **Mortality rate:** 2%  
- **Recovery time:** 10 time steps  
- **15% non-compliance with distancing**

---

### Policy Experiments
#### A. Distancing Compliance Variants
- Increase non-compliance to 25%  
- Increase non-compliance to 40%


#### B. Immunity Variability
- Change post-recovery immunity distribution to N(0.5, 0.2)  
- Fixed 100% immunity

---

### Reporting
A Final Report was created analyzing our results

---
