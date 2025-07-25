import matplotlib.pyplot as plt
import numpy as np

# Scenario labels
scenarios = ['Rapid Outbreak', 'Balanced Spread', 'Slow Spread']

# Time steps (example values)
no_cdc = [99.8, 89.33, 22.4]  # Red [Rapid, Balanced, Slow]
cdc = [99.5, 85.73, ]     # Blue [Rapid, Balanced, Slow]

# X locations
x = np.arange(len(scenarios))  # [0, 1, 2]
bar_width = 0.35

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))

# Bars
bars1 = ax.bar(x - bar_width/2, no_cdc, bar_width, label='No CDC Intervention', color='red')
bars2 = ax.bar(x + bar_width/2, cdc, bar_width, label='CDC Intervention', color='blue')

# Labels and titles
ax.set_xlabel('Scenario')
ax.set_ylabel('Percentage of Population')
ax.set_title('Effect of CDC Intervention on Peak Infected')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.legend()

# Optional: add data labels
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()
