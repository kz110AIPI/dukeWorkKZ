import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to process each CSV file and create an overlapped bar graph
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
    
    # Group data by chromosome and calculate mean values if multiple regions exist on the same chromosome
    chr_data = data.groupby('CHR').agg({
        'Invasive_Value': 'mean',
        'Non_Invasive_Value': 'mean'
    }).reset_index()

    # Plot the data
    plt.figure(figsize=(12, 7))
    width = 0.4  # Width of the bars
    x = range(len(chr_data))  # x locations for each chromosome

    # Plot invasive and non-invasive values as overlapped bars for each chromosome
    plt.bar(x, chr_data['Invasive_Value'], width, label='Invasive Log2 Ratio', color='blue', alpha=0.6)
    plt.bar(x, chr_data['Non_Invasive_Value'], width, label='Non-Invasive Log2 Ratio', color='orange', alpha=0.6)
    
    # Set labels and title
    plt.xlabel('Chromosome (CHR)')
    plt.ylabel('Average Log2 Ratio')
    plt.title(f'Average CNV Log2 Ratio by Chromosome for {csv_file}')
    plt.xticks(x, chr_data['CHR'])
    plt.legend()
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(f"{csv_file.replace('.csv', '')}_bar_plot.png")
    plt.show()

# Process and plot each CSV file in the current directory
for csv_file in glob.glob("*.csv"):
    plot_cnv_bar(csv_file)
