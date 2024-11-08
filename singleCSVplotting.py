import pandas as pd
import matplotlib.pyplot as plt

# Load the actual data from the provided file
data = pd.read_csv('352__ADH_full_range.csv')

# Convert Region_Type to numerical values for plotting
data['Value'] = data['Region_Type'].apply(lambda x: 1 if x == 'Gain' else (-1 if x == 'Loss' else 0))
data['Region_Length'] = data['END'] - data['START']

# Calculate cumulative positions, separating chromosomes
spacing = 1000000  # Space between chromosomes for visual separation
data['Position'] = 0  # Initialize Position column

# Start from the beginning and calculate positions
current_position = 0
chromosome_end_positions = []  # To store the end positions of each chromosome

for chr_num in sorted(data['CHR'].unique()):
    chr_data = data[data['CHR'] == chr_num]
    data.loc[chr_data.index, 'Position'] = current_position + chr_data['Region_Length'].cumsum().shift(fill_value=0)
    current_position = data.loc[chr_data.index, 'Position'].iloc[-1] + spacing
    chromosome_end_positions.append(current_position)  # Save end position of each chromosome

# Plot each chromosome region in sequence with color-coded region types
plt.figure(figsize=(12, 6))

for i, row in data.iterrows():
    color = 'red' if row['Value'] == 1 else ('blue' if row['Value'] == -1 else 'white')
    plt.barh(y=0, width=row['Region_Length'], left=row['Position'], color=color, align='edge')

# Add chromosome labels
chr_ticks = data.groupby('CHR')['Position'].first() + data.groupby('CHR')['Region_Length'].sum() / 2
plt.xticks(chr_ticks, sorted(data['CHR'].unique()))

# Add vertical lines between chromosomes
for pos in chromosome_end_positions[:-1]:  # Exclude the last position as it doesn't need a line after it
    plt.axvline(x=pos, color='black', linestyle='--', linewidth=0.5)

# Customize plot
plt.xlabel("Chromosome Number")
plt.ylabel("Region Type Indicator")
plt.title("Chromosome Regions with Gains and Losses")
plt.yticks([])  # Hide y-axis ticks for a cleaner look
plt.legend(handles=[
    plt.Line2D([0], [0], color='red', lw=4, label='Gain'),
    plt.Line2D([0], [0], color='blue', lw=4, label='Loss'),
], loc="upper right")
plt.tight_layout()
plt.show()
