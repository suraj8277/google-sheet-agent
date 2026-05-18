import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import argparse

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
    parser = argparse.ArgumentParser(description="Advanced Visual Brain for Excel")
    parser.add_argument("--input", required=True, help="Input Excel/CSV file")
    parser.add_argument("--sheet", default=0, help="Sheet name or index")
    parser.add_argument("--type", choices=["bar", "pie", "line", "scatter"], required=True, help="Chart type")
    parser.add_argument("--x", required=True, help="X-axis column")
    parser.add_argument("--y", help="Y-axis column (if not provided, a count will be used)")
    parser.add_argument("--output", default="chart.png", help="Output PNG path")
    parser.add_argument("--title", help="Chart title")

    args = parser.parse_args()
    
    df = load_file(args.input, args.sheet)
    
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    title = args.title or f"{args.type.capitalize()} Chart: {args.x}"
    
    if args.type == "bar":
        if args.y:
            sns.barplot(data=df, x=args.x, y=args.y)
        else:
            sns.countplot(data=df, x=args.x)
    
    elif args.type == "pie":
        data = df[args.x].value_counts()
        plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
    
    elif args.type == "line":
        if not args.y:
            print("Error: Line chart requires --y column")
            sys.exit(1)
        sns.lineplot(data=df, x=args.x, y=args.y)
        
    elif args.type == "scatter":
        if not args.y:
            print("Error: Scatter chart requires --y column")
            sys.exit(1)
        sns.scatterplot(data=df, x=args.x, y=args.y)

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Success! Chart saved to {args.output}")

if __name__ == "__main__":
    main()
