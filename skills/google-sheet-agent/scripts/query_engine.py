import pandas as pd
import sys
import os
import argparse
import traceback

def load_file(file_path, sheet_name=0):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            raise ValueError(f"Unsupported format: {ext}")
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Smart Query Brain for Excel")
    parser.add_argument("--input", required=True, help="Input Excel/CSV file")
    parser.add_argument("--sheet", default=0, help="Sheet name or index")
    parser.add_argument("--code", required=True, help="Python code snippet to execute on 'df'")
    parser.add_argument("--output", help="Optional output file path if data is modified")

    args = parser.parse_args()
    
    df = load_file(args.input, args.sheet)
    
    # Environment for execution
    local_vars = {'df': df, 'pd': pd}
    
    try:
        # We execute the code. The code should ideally assign the result to a variable 'result' 
        # or just modify 'df'.
        exec(args.code, {}, local_vars)
        
        if 'result' in local_vars:
            print("\n--- Query Result ---")
            print(local_vars['result'])
        else:
            print("\nCode executed successfully. (No 'result' variable found to print)")
            
        if args.output and 'df' in local_vars:
            ext = os.path.splitext(args.output)[-1].lower()
            if ext == '.csv':
                local_vars['df'].to_csv(args.output, index=False)
            else:
                local_vars['df'].to_excel(args.output, index=False)
            print(f"Modified data saved to {args.output}")

    except Exception:
        print("\nError executing smart query:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
