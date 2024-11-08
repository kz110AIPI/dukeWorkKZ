import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to process each CSV file and create a scatter plot
def plot_cnv_scatter(csv_file):
    # Load data
    data = pd.read_csv(csv_file)
    
    # Print columns to verify names
    print(f"Columns in {csv_file}: {data.columns}")

    # Check if the expected columns exist, update if necessary
    if 'Invasive_Value' not in data.columns or 'Non_Invasive_Value' not in data.columns:
        print(f"Error: 'Invasive_Value' or 'Non_Invasive_Value' column not found in {csv_file}.")
        return

    # Filter data into gains and losses for color coding
    gains = data[data['Invasive_Value'] > 0]
    losses = data[data['Invasive_Value'] < 0]
    
    # Create scatter plot
    plt.figure(figsize=(12, 7))
    
    # Plot gains and losses with different colors
    plt.scatter(gains['CHR'], gains['Overlap_Start'], c='blue', label='Gain (Invasive)', alpha=0.6)
    plt.scatter(gains['CHR'], gains['Overlap_End'], c='lightblue', label='Gain (Non-Invasive)', alpha=0.6, marker='x')
    plt.scatter(losses['CHR'], losses['Overlap_Start'], c='red', label='Loss (Invasive)', alpha=0.6)
    plt.scatter(losses['CHR'], losses['Overlap_End'], c='salmon', label='Loss (Non-Invasive)', alpha=0.6, marker='x')

    # Set labels and title
    plt.xlabel('Chromosome (CHR)')
    plt.ylabel('Location (Overlap Start/End)')
    plt.title(f'CNV Overlapping Regions by Chromosome for {csv_file}')
    plt.legend()
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(f"{csv_file.replace('.csv', '')}_scatter_plot.png")
    plt.show()

# Process and plot each CSV file in the current directory
for csv_file in glob.glob("*.csv"):
    plot_cnv_scatter(csv_file)
