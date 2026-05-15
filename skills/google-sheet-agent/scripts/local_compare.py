import pandas as pd
import sys
import os

def load_file(file_path):
    """Loads a CSV or Excel file into a DataFrame."""
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            print(f"Error: Unsupported file format '{ext}' for file {file_path}")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        sys.exit(1)

def main(old_file, new_file, key_column, output_file):
    print(f"Loading files: '{old_file}' and '{new_file}'...")
    old_df = load_file(old_file)
    new_df = load_file(new_file)
    
    if key_column not in old_df.columns or key_column not in new_df.columns:
        print(f"Error: Key column '{key_column}' not found in one of the files.")
        print(f"Old columns: {list(old_df.columns)}")
        print(f"New columns: {list(new_df.columns)}")
        sys.exit(1)

    print(f"Comparing data using key: '{key_column}'...")
    
    # Ensure key column is string for consistent matching
    old_df[key_column] = old_df[key_column].astype(str)
    new_df[key_column] = new_df[key_column].astype(str)

    # Set index for merging/updating
    old_df.set_index(key_column, inplace=True)
    
    # We create a copy of the 'New' data to perform updates on
    result_df = new_df.copy()
    result_df.set_index(key_column, inplace=True)

    # 1. Update existing rows in New with data from Old
    # 2. Add rows from Old that are missing in New
    
    # Combine data: prioritizes values from 'old_df' where indices match
    # but keeps everything else from 'result_df'
    updated_df = old_df.combine_first(result_df)
    
    # Reset index to bring key_column back as a column
    updated_df.reset_index(inplace=True)

    print(f"Saving merged results to '{output_file}'...")
    
    ext = os.path.splitext(output_file)[-1].lower()
    if ext == '.csv':
        updated_df.to_csv(output_file, index=False)
    else:
        updated_df.to_excel(output_file, index=False)

    print(f"Success! Merged data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python local_compare.py <old_file> <new_file> <key_column> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
