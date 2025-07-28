import matplotlib.pyplot as plt
import numpy as np

# X-axis groups (Scenarios)
scenarios = ['Slow Spread', 'Balanced Spread', 'Rapid Spread']
x = np.arange(len(scenarios))  # [0, 1, 2]

# Y-axis values for each group of bars
nonCompliance_010 = [1.51, 1.97, 2.02]
nonCompliance_025 = [1.73, 1.95, 1.88]
nonCompliance_040 = [2.09, 1.87, 1.96]
nonCompliance_100 = [2.04, 1.88, 1.97]

# Bar width and positions
bar_width = 0.2
offsets = [-1.5, -0.5, 0.5, 1.5]  # Even spacing around center

# Plot setup
fig, ax = plt.subplots(figsize=(12, 6))

# Plot bars for each compliance level
bars010 = ax.bar(x + offsets[0]*bar_width, nonCompliance_010, bar_width, label='10% Non-Compliance', color='#4daf4a')
bars025 = ax.bar(x + offsets[1]*bar_width, nonCompliance_025, bar_width, label='25% Non-Compliance', color='#377eb8')
bars040 = ax.bar(x + offsets[2]*bar_width, nonCompliance_040, bar_width, label='40% Non-Compliance', color='#ff7f00')
bars100 = ax.bar(x + offsets[3]*bar_width, nonCompliance_100, bar_width, label='100% Non-Compliance', color='#e41a1c')

# Labels and titles
ax.set_xlabel('Scenario')
ax.set_ylabel('Total Percent of Populations (%)')
ax.set_title('Effect of Non-Compliance Rates on Average Peak Dead')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.legend(title='Distancing Compliance')

# Optional: Add data labels
for bar_group in [bars010, bars025, bars040, bars100]:
    for bar in bar_group:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

plt.tight_layout()
plt.show()
