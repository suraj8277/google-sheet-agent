import pandas as pd
import sys
import os
import argparse

def load_file(file_path, sheet_name=None):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            # If sheet_name is None, it reads the first sheet. 
            # If it's a list or "None" (in read_excel terms), it reads multiple.
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            raise ValueError(f"Unsupported format: {ext}")
    except Exception as e:
        print(f"Error loading {file_path} (Sheet: {sheet_name}): {str(e)}")
        sys.exit(1)

def save_file(data, output_path):
    ext = os.path.splitext(output_path)[-1].lower()
    try:
        if isinstance(data, dict):
            # Multiple sheets
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # Single sheet
            if ext == '.csv':
                data.to_csv(output_path, index=False)
            else:
                data.to_excel(output_path, index=False)
        print(f"File saved to {output_path}")
    except Exception as e:
        print(f"Error saving to {output_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Sheet Excel Processor")
    parser.add_argument("command", choices=["merge", "join", "filter", "sort", "aggregate", "dedupe", "summary", "rename", "drop"])
    parser.add_argument("--input", help="Primary input file", required=True)
    parser.add_argument("--sheet", help="Sheet name in primary file (use 'ALL' for batch operations)", default=0)
    parser.add_argument("--input2", help="Second input file")
    parser.add_argument("--sheet2", help="Sheet name in second file", default=0)
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--column", help="Target column(s)")
    parser.add_argument("--value", help="Value for filtering/renaming")
    parser.add_argument("--key", help="Key column for merge/join")
    parser.add_argument("--how", choices=["left", "right", "inner", "outer"], default="inner")

    args = parser.parse_args()
    
    # Resolve 'ALL' logic
    if args.sheet == "ALL":
        xl = pd.ExcelFile(args.input)
        sheets_to_process = xl.sheet_names
    else:
        # If it's a digit, convert to int (index), otherwise keep as name
        try:
            sheets_to_process = [int(args.sheet)]
        except ValueError:
            sheets_to_process = [args.sheet]

    output_data = {}
    is_batch = len(sheets_to_process) > 1

    for sn in sheets_to_process:
        print(f"Processing sheet: {sn}...")
        df = load_file(args.input, sheet_name=sn)
        
        # Determine actual sheet name for dict keys
        actual_name = sn if isinstance(sn, str) else f"Sheet_{sn}"

        if args.command == "summary":
            print(f"\n--- Summary for {actual_name} ---")
            print(f"Rows: {len(df)} | Columns: {list(df.columns)}")
            print(df.describe())
            continue

        result = df
        if args.command == "merge":
            df2 = load_file(args.input2, sheet_name=args.sheet2)
            df.set_index(args.key, inplace=True)
            df2.set_index(args.key, inplace=True)
            result = df2.combine_first(df).reset_index()

        elif args.command == "join":
            df2 = load_file(args.input2, sheet_name=args.sheet2)
            result = pd.merge(df, df2, on=args.key, how=args.how)

        elif args.command == "filter":
            try:
                val = float(args.value)
                result = df[df[args.column] == val]
            except ValueError:
                result = df[df[args.column].astype(str).str.contains(args.value, case=False, na=False)]

        elif args.command == "sort":
            cols = args.column.split(',')
            ascending = args.value.lower() != "desc" if args.value else True
            result = df.sort_values(by=cols, ascending=ascending)

        elif args.command == "aggregate":
            result = df.groupby(args.column).sum(numeric_only=True).reset_index()

        elif args.command == "dedupe":
            cols = args.column.split(',') if args.column else None
            result = df.drop_duplicates(subset=cols)

        elif args.command == "rename":
            mapping = dict(zip(args.column.split(','), args.value.split(',')))
            result = df.rename(columns=mapping)

        elif args.command == "drop":
            cols = args.column.split(',')
            result = df.drop(columns=cols)

        output_data[actual_name] = result

    if args.command != "summary":
        final_output = args.output or f"processed_{os.path.basename(args.input)}"
        if is_batch:
            save_file(output_data, final_output)
        else:
            # Save just the single DataFrame
            save_file(list(output_data.values())[0], final_output)

if __name__ == "__main__":
    main()
