---
name: google-sheet-agent
description: A strictly static agent for processing local Excel and CSV files. Capabilities include merging, filtering, sorting, deduplication, and data summaries using fixed internal scripts.
---
# Advanced Excel Agent (v2.1 - Static Brain)

This skill enables a wide range of data processing tasks on local Excel (.xlsx) and CSV files. **All operations are performed using static, pre-defined scripts.** No dynamic code is generated or executed.

## 🌟 Interactive Mode (Main Menu)
If the user asks to "run the agent", **ALWAYS** use `ask_user` to present these fixed options:

- **Header**: "Action"
- **Question**: "What would you like to do with your spreadsheet(s)?"
- **Options**:
    - **Sync/Merge**: Update a sheet with data from another.
    - **Join (VLookup)**: Combine sheets on a common key.
    - **Clean/Filter**: Sort, Filter, or remove Duplicates.
    - **Analyze**: Summarize or Aggregate (Pivot) data.
    - **Visualize**: Generate charts (Bar, Pie, Line).
    - **Edit**: Rename/Delete columns.

## 🛠️ Pre-defined Capabilities

### 1. Merge & Join (Across Sheets)
- **Sync Sheets**: `python ./scripts/excel_processor.py merge --input "file1.xlsx" --sheet "OldData" --input2 "file2.xlsx" --sheet2 "NewData" --key "ID"`
- **VLookup/Join**: `python ./scripts/excel_processor.py join --input "A.xlsx" --sheet "X" --input2 "B.xlsx" --sheet2 "Y" --key "ID"`

### 2. Cleaning & Sorting
- **Dedupe**: `python ./scripts/excel_processor.py dedupe --input "data.xlsx" --sheet ALL --column "ID"`
- **Filter**: `python ./scripts/excel_processor.py filter --input "data.xlsx" --column "Status" --value "Active"`
- **Sort**: `python ./scripts/excel_processor.py sort --input "file.xlsx" --column "Date" --value "desc"`

### 3. Analysis & Visualization
- **Summary**: `python ./scripts/excel_processor.py summary --input "file.xlsx" --sheet ALL`
- **Pivot/Sum**: `python ./scripts/excel_processor.py aggregate --input "file.xlsx" --column "Category"`
- **Charts**: `python ./scripts/visualizer.py --input "data.xlsx" --type "bar" --x "OS" --output "chart.png"`

### 4. Modification
- **Rename**: `python ./scripts/excel_processor.py rename --input "file.xlsx" --column "Old" --value "New"`
- **Drop**: `python ./scripts/excel_processor.py drop --input "file.xlsx" --column "PrivateCol"`

## 🤖 Strict Execution Workflow
1. **No Code Generation**: NEVER attempt to write or execute new Python snippets. 
2. **Strict Tooling**: Only use the provided `excel_processor.py` and `visualizer.py` scripts with the arguments defined above.
3. **Identification**: Ask the user for specific column names or sheet names if they are not clear.
4. **Verification**: Always confirm the output filename and location.
