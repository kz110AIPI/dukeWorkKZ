import pandas as pd

# Load CSV files
invasive_df = pd.read_csv('inv_tumor_call_table.csv')
non_invasive_df = pd.read_csv('noniv_tumor_call_table.csv')

# Function to find overlapping CNV regions with the same gain or loss type
def find_matching_cnv(invasive_sample, non_invasive_sample):
    # Filter invasive and non-invasive samples based on chromosome changes
    invasive_changes = invasive_sample[(invasive_sample['Value'] != 0)]
    non_invasive_changes = non_invasive_sample[(non_invasive_sample['Value'] != 0)]
    
    # Initialize list to store matching overlapping regions
    matching_regions = []
    
    # Loop over invasive changes and check for overlap with non-invasive changes of the same type
    for _, inv_row in invasive_changes.iterrows():
        inv_chr, inv_start, inv_end, inv_value = inv_row['CHR'], inv_row['START'], inv_row['END'], inv_row['Value']
        
        # Check for overlaps in non-invasive data with the same type (gain or loss)
        same_type_overlaps = non_invasive_changes[
            (non_invasive_changes['CHR'] == inv_chr) &
            (non_invasive_changes['START'] <= inv_end) &
            (non_invasive_changes['END'] >= inv_start) &
            (non_invasive_changes['Value'].apply(lambda x: (x > 0 and inv_value > 0) or (x < 0 and inv_value < 0)))
        ]
        
        # Append overlapping regions with the same CNV type
        for _, non_inv_row in same_type_overlaps.iterrows():
            overlap_start = max(inv_start, non_inv_row['START'])
            overlap_end = min(inv_end, non_inv_row['END'])
            region_data = {
                'CHR': inv_chr,
                'Overlap_Start': overlap_start,
                'Overlap_End': overlap_end,
                'Invasive_Value': inv_value,
                'Non_Invasive_Value': non_inv_row['Value'],
                'Region_Type': 'Gain' if inv_value > 0 else 'Loss'
            }
            matching_regions.append(region_data)
    
    return matching_regions

# Compare all invasive samples with corresponding non-invasive samples
def compare_samples(invasive_df, non_invasive_df):
    results = []
    
    for sample in invasive_df.columns[3:]:  # Exclude CHR, START, END columns
        for suffix in ['_ADH', '_Hyperplasia', '_DCIS']:
            non_inv_sample = f"{sample}{suffix}"
            
            if non_inv_sample in non_invasive_df.columns:
                invasive_data = invasive_df[['CHR', 'START', 'END', sample]].rename(columns={sample: 'Value'})
                non_invasive_data = non_invasive_df[['CHR', 'START', 'END', non_inv_sample]].rename(columns={non_inv_sample: 'Value'})
                
                matching_regions = find_matching_cnv(invasive_data, non_invasive_data)
                results.extend(matching_regions)
    
    # Convert results to DataFrame and save
    overlap_df = pd.DataFrame(results)
    overlap_df.to_csv('cnv_matching_overlaps.csv', index=False)
    print("Comparison complete. Results saved to 'cnv_matching_overlaps.csv'.")

# Run comparison
compare_samples(invasive_df, non_invasive_df)
