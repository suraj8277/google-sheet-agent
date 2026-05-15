import gspread
import pandas as pd
import sys
import os
import json

def main(old_sheet_name, new_sheet_name, key_column):
    # Path to credentials
    creds_path = os.path.join(os.path.dirname(__file__), '..', 'service_account.json')
    
    if not os.path.exists(creds_path):
        print(f"Error: {creds_path} not found. Please place your Google Service Account JSON file there.")
        sys.exit(1)

    try:
        # Authenticate
        gc = gspread.service_account(filename=creds_path)
        
        print(f"Opening sheets: '{old_sheet_name}' and '{new_sheet_name}'...")
        old_sh = gc.open(old_sheet_name).sheet1
        new_sh = gc.open(new_sheet_name).sheet1
        
        # Load into Pandas
        old_df = pd.DataFrame(old_sh.get_all_records())
        new_df = pd.DataFrame(new_sh.get_all_records())
        
        if key_column not in old_df.columns or key_column not in new_df.columns:
            print(f"Error: Key column '{key_column}' not found in one of the sheets.")
            sys.exit(1)

        print("Comparing data...")
        # Set index to the key column for easy comparison
        old_df.set_index(key_column, inplace=True)
        new_df.set_index(key_column, inplace=True)
        
        # Identify rows in Old that are different or missing in New
        # For this agent, we'll focus on updating New with Old's data where they match keys,
        # or adding missing rows from Old to New if that's the intent.
        
        # Update existing keys in New with values from Old
        updates_count = 0
        for index, row in old_df.iterrows():
            if index in new_df.index:
                if not row.equals(new_df.loc[index]):
                    # Update the row in the actual Google Sheet
                    # Find the row number in New Sheet (index + 2 because 1-based and header)
                    # This is a simple implementation; for large sheets, batch updates are better.
                    row_idx = new_df.index.get_loc(index) + 2
                    new_sh.update(f"A{row_idx}", [row.tolist()])
                    updates_count += 1
            else:
                # Append missing row to New
                new_sh.append_row([index] + row.tolist())
                updates_count += 1

        print(f"Success! Processed {updates_count} updates/additions in '{new_sheet_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python compare_and_update.py <old_sheet> <new_sheet> <key_column>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
