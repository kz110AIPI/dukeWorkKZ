import pandas as pd

# Load CSV files
invasive_df = pd.read_csv('data/inv_tumor_call_table.csv')
non_invasive_df = pd.read_csv('data/noniv_tumor_call_table.csv')

# Function to find overlapping CNV regions with the same gain or loss type
def find_matching_cnv(invasive_sample, non_invasive_sample, full_template):
    # Initialize list to store results with entire chromosome range
    results = full_template.copy()
    results['Region_Type'] = 0  # Default to 0 for non-overlapping regions

    # Loop over invasive changes and check for overlap with non-invasive changes of the same type
    for _, inv_row in invasive_sample.iterrows():
        inv_chr, inv_start, inv_end, inv_value = inv_row['CHR'], inv_row['START'], inv_row['END'], inv_row['Value']
        
        # Check for overlaps in non-invasive data with the same type (gain or loss)
        same_type_overlaps = non_invasive_sample[
            (non_invasive_sample['CHR'] == inv_chr) &
            (non_invasive_sample['START'] <= inv_end) &
            (non_invasive_sample['END'] >= inv_start) &
            (non_invasive_sample['Value'].apply(lambda x: (x > 0 and inv_value > 0) or (x < 0 and inv_value < 0)))
        ]
        
        # Update overlapping regions in the full template
        for _, non_inv_row in same_type_overlaps.iterrows():
            overlap_start = max(inv_start, non_inv_row['START'])
            overlap_end = min(inv_end, non_inv_row['END'])
            
            # Update matching rows in the results with the Region_Type information
            overlap_mask = (results['CHR'] == inv_chr) & \
                           (results['START'] <= overlap_end) & \
                           (results['END'] >= overlap_start)
            results.loc[overlap_mask, 'Region_Type'] = 'Gain' if inv_value > 0 else 'Loss'

    return results

# Compare all invasive samples with corresponding non-invasive samples and save each comparison to a separate CSV file
def compare_samples(invasive_df, non_invasive_df):
    for sample in invasive_df.columns[3:]:  # Exclude CHR, START, END columns
        for suffix in ['_ADH', '_Hyperplasia', '_DCIS']:
            non_inv_sample = f"{sample}{suffix}"
            
            if non_inv_sample in non_invasive_df.columns:
                invasive_data = invasive_df[['CHR', 'START', 'END', sample]].rename(columns={sample: 'Value'})
                non_invasive_data = non_invasive_df[['CHR', 'START', 'END', non_inv_sample]].rename(columns={non_inv_sample: 'Value'})
                
                # Use the full range of chromosome regions as the template
                full_template = invasive_df[['CHR', 'START', 'END']].drop_duplicates().reset_index(drop=True)
                
                matching_regions = find_matching_cnv(invasive_data, non_invasive_data, full_template)
                
                # Save the results with full chromosome range and mapped Region_Type
                output_filename = f"{sample}_{suffix}_full_range.csv"
                matching_regions.to_csv(output_filename, index=False)
                print(f"Results saved to '{output_filename}'.")

# Run comparison
compare_samples(invasive_df, non_invasive_df)
