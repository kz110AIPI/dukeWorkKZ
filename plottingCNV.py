import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to process each CSV file and create a bar graph
def plot_cnv_bar(csv_file):
    # Load data
    data = pd.read_csv(csv_file)
    
    # Verify the required columns are present
    required_columns = {'CHR', 'Overlap_Start', 'Overlap_End', 'Invasive_Value', 'Non_Invasive_Value'}
    if not required_columns.issubset(data.columns):
        print(f"Error: One or more required columns are missing in {csv_file}.")
        return

    # Sort data by chromosome and start position for plotting in order
    data = data.sort_values(by=['CHR', 'Overlap_Start'])
    
    # Create a new column for the x-axis labels that combines CHR and the region range
    data['CHR_Region'] = data['CHR'].astype(str) + ":" + data['Overlap_Start'].astype(str) + "-" + data['Overlap_End'].astype(str)
    
    # Plot the data
    plt.figure(figsize=(12, 7))
    x = range(len(data))  # x locations for each region

    # Plot stacked bars for Invasive and Non-Invasive values
    plt.bar(x, data['Invasive_Value'], label='Invasive Log2 Ratio', color='blue', alpha=0.6)
    plt.bar(x, data['Non_Invasive_Value'], bottom=data['Invasive_Value'], label='Non-Invasive Log2 Ratio', color='orange', alpha=0.6)
    
    # Set labels and title
    plt.xlabel('Chromosome and Region (CHR:Start-End)')
    plt.ylabel('Log2 Ratio')
    plt.title(f'CNV Log2 Ratio by Chromosome Region for {csv_file}')
    plt.xticks(x, data['CHR_Region'], rotation=90)
    plt.legend()
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(f"{csv_file.replace('.csv', '')}_bar_plot.png")
    plt.show()

# Process and plot each CSV file in the current directory
for csv_file in glob.glob("*.csv"):
    plot_cnv_bar(csv_file)
