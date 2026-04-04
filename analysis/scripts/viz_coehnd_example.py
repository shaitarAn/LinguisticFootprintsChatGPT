import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Define means and standard deviation for two distributions
mean_a, mean_b = 0, 1.5  # Keeping them apart to show the difference
std = 1

# Define x range for plotting
x = np.linspace(-4, 6, 500)

# Create distributions using norm.pdf from scipy.stats
y_a = norm.pdf(x, mean_a, std)
y_b = norm.pdf(x, mean_b, std)

# Plot the two distributions
ax.plot(x, y_a, label="Group A", color='blue', linewidth=2)
ax.plot(x, y_b, label="Group B", color='orange', linewidth=2)

# Mark the means of the distributions with vertical dashed lines
ax.axvline(mean_a, color='blue', linestyle='--', linewidth=2, label="Mean A")
ax.axvline(mean_b, color='orange', linestyle='--', linewidth=2, label="Mean B")

# Draw a horizontal line with arrow ends to indicate the difference between the means
ax.annotate("", xy=(mean_a, 0.1), xytext=(mean_b, 0.1),
            arrowprops=dict(arrowstyle="<->", color='black', linewidth=2))
ax.text((mean_a + mean_b) / 2, 0.12, 'Difference', ha='center', fontsize=12, weight='bold')

# Set labels and title
ax.set_xlabel('Score')
ax.set_ylabel('Density')
ax.set_title("Cohen's d: Visual Representation of Effect Size", fontsize=16)

# Add a legend
# ax.legend()

# Show the plot
plt.tight_layout()
plt.savefig("../../viz/cohen_d_simple_visual.png", format='png')
plt.show()
