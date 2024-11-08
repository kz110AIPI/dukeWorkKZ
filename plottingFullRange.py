import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Load each full-range dataset and plot as a bar graph
def plot_full_range_datasets(folder_path):
    # Get all full-range CSV files in the folder
    file_paths = glob.glob(f"{folder_path}/*_full_range.csv")
    
    for file_path in file_paths:
        # Load data
        data = pd.read_csv(file_path)

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
        plt.xlabel("Chromosome Location")
        plt.ylabel("Gene Gain/Loss")
        #plt.title(f"{file_path.replace('_full_range.csv', '')} Shared CNV Comparision")
        # Extract the base name (file name only) and remove the suffix
        file_name = os.path.basename(file_path).replace('_full_range.csv', '')

        # Set the title with the modified file name
        plt.title(f"{file_name} CNV Comparison")
        plt.yticks([])  # Hide y-axis ticks for a cleaner look
        plt.legend(handles=[
            plt.Line2D([0], [0], color='red', lw=4, label='Gain'),
            plt.Line2D([0], [0], color='blue', lw=4, label='Loss'),
        ], loc="upper right")
        plt.tight_layout()
        # Save and show the plot
        plt.savefig(f"{file_path.replace('.csv', '')}_bar_plot.png")
        plt.show()


# Specify the folder where the full-range datasets are saved
folder_path = "fullRangeData"
plot_full_range_datasets(folder_path)
