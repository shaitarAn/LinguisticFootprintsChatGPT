import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create a slide presenting MTLD visually with arches over the TTR threshold.

# Initialize the figure
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('Measure of Textual Lexical Diversity (MTLD)', fontsize=18, weight='bold')

# Defining the TTR threshold
threshold = 0.72
ax.axhline(y=threshold, color='r', linestyle='--', linewidth=1, label='TTR Threshold (0.72)')

# Simulating different segments with varying widths
segments = [300, 250, 200, 400, 350, 120, 500]  # Different segment word counts
cumulative_words = np.cumsum(segments)

# Creating the arches that represent TTR values across segments
for i, segment in enumerate(segments):
    # Define the arch's x-coordinates
    start_x = cumulative_words[i] - segment
    end_x = cumulative_words[i]
    midpoint_x = (start_x + end_x) / 2

    # Define the width and height of each arch (height corresponds to TTR value)
    arch_height = threshold + (0.1 + (i % 3) * 0.05)  # Varying heights between 0.82 and 0.87
    arch_width = segment / 2  # Width is proportional to the number of words in the segment

    # Generate x values for half-circle (arch)
    x_vals = np.linspace(start_x, end_x, 100)
    y_vals = np.sqrt((arch_width ** 2) - ((x_vals - midpoint_x) ** 2)) / arch_width
    y_vals = (y_vals * (arch_height - threshold)) + threshold

    # Plotting the arch
    ax.plot(x_vals, y_vals, color='blue', linewidth=2)

# Setting labels and other plot properties
ax.set_xlabel("Number of Words (Cumulative)", fontsize=14)
ax.set_ylabel("Type-Token Ratio (TTR)", fontsize=14)
ax.yaxis.label.set_size(16)
ax.xaxis.label.set_size(16)
ax.set_xticks(cumulative_words)
ax.legend(fontsize=12)
ax.grid(visible=True)

# Adding the MTLD calculation as a text annotation
# MTLD = N / NS
N_words = sum(segments)  # Total words in the text (all segments combined)
NS_segments = len(segments)  # Number of segments with TTR above threshold (in this example all are above)
mtld_value = N_words / NS_segments

calculation_text = (
    fr"$\mathrm{{MTLD}} = \frac{{N}}{{NS}} = \frac{{{N_words}}}{{{NS_segments}}} \approx {N_words / NS_segments:.2f}$" + "\n\n"
    r"$N$: Total Number of Words in the Text" + "\n"
    r"$NS$: Number of Segments with TTR $\geq 0.72$"
)
ax.text(0.2, 0.36, calculation_text, transform=ax.transAxes, fontsize=16,
        verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor='white'))

# Saving the figure
# plt.tight_layout(rect=[0, 0.05, 0.9, 0.9])  # Adjust layout to accommodate title and text box
plt.tight_layout()
plt.savefig("mtld_arches_visualization.png", format='png')
# plt.show()

# ####################

# Create a slide presenting Yule's I visually and including the calculation.

# Initialize the figure
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle("Yule's I - Balancing Repetition and Diversity", fontsize=16, weight='bold')

# Data to simulate word frequency distribution
words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
frequencies = [10, 7, 5, 4, 3, 2, 2, 1]  # Simulated frequencies of words

# Creating a bar chart for word frequency distribution
bars = ax.bar(words, frequencies, color='green', alpha=0.7)
ax.set_xlabel("Unique Words", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)
ax.set_yticks(range(0, 12, 2))
# ax.set_title("Word Frequency Distribution", fontsize=14, y=1.06)

# Adding the Yule's I calculation as a text annotation
# Assuming values for explanation purposes
unique_words = len(words)  # |V|, number of unique words
M = sum(f ** 2 for f in frequencies)  # Sum of squared frequencies

# Calculate Yule's I
yules_I = unique_words ** 2 / (M - unique_words)

calculation_text = (
    fr"$\mathrm{{Yule's\ I}} = \frac{{|V|^2}}{{M - |V|}} = \frac{{{unique_words}^2}}{{{M} - {unique_words}}} = 0.32$" + "\n\n"
    r"$|V|$: Number of Unique Words = " + f"{unique_words}" + "\n"
    r"$M$: Sum of Squared Frequencies = " + f"{M}" + "\n"
)

# Adding the formula and calculation on the plot
ax.text(0.35, 0.7, calculation_text, transform=ax.transAxes, fontsize=16,
        verticalalignment='center', bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor='white'))

# Adding a horizontal line for better visualization of repetitiveness threshold
# ax.axhline(y=np.mean(frequencies), color='r', linestyle='--', linewidth=1, label='Average Frequency')
# ax.legend()

# Adjusting layout and saving the figure
# plt.tight_layout(rect=[0, 0.05, 0.9, 0.95])  # Adjust layout to accommodate title and text box
plt.tight_layout()
plt.savefig("yules_I_visualization_with_calculation.png", format='png')
plt.show()


# ####################
# make a slide for TTR with just the formula and a simple example

# Initialize the figure
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle("Type-Token Ratio (TTR) - Lexical Diversity", fontsize=16, weight='bold')

# Adding the TTR formula and a simple example
formula_text = r"$\mathrm{TTR} = \frac{|V|}{N}$" + "\n\n" + r"$|V|$: Number of Unique Words" + "\n" + r"$N$: Total Number of Words"

example_text = (
    "Example:" + "\n"
    "Total Words: 100" + "\n"
    "Unique Words: 50" + "\n\n"
    r"$\mathrm{TTR} = \frac{50}{100} = 0.5$"
)

# Adding the formula and example on the plot
ax.text(0.35, 0.5, formula_text, transform=ax.transAxes, fontsize=16,
        verticalalignment='center', bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor='white'))
ax.text(0.35, 0.2, example_text, transform=ax.transAxes, fontsize=16, verticalalignment='center', bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor='white'))

# Adjusting layout and saving the figure
plt.tight_layout()
# plt.savefig("ttr_formula_and_example.png", format='png')
# plt.show()
