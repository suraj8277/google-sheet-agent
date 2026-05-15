---
name: google-sheet-agent
description: An advanced agent for processing local Excel and CSV files. Capabilities include multi-sheet support, merging, filtering, sorting, deduplication, and data summaries.
---
# Advanced Excel Agent

This skill enables a wide range of data processing tasks on local Excel (.xlsx) and CSV files, including full support for multi-sheet workbooks.

## Multi-Sheet Operations
You can target specific sheets or process all sheets at once.
- **Specific Sheet**: Use `--sheet "SheetName"` or `--sheet 1` (0-based index).
- **All Sheets (Batch)**: Use `--sheet ALL`. This will apply your command (like `dedupe` or `filter`) to every tab in the file and save a multi-sheet output.

## Interactive Mode (Main Menu)
If the user is vague or asks to "run the agent", **ALWAYS** use `ask_user` to present these options:

- **Header**: "Action"
- **Question**: "What would you like to do with your spreadsheet(s)?"
- **Options**:
    - **Sync/Merge**: Update a sheet with data from another.
    - **Batch Process**: Apply a clean/filter rule to ALL sheets.
    - **Join (VLookup)**: Combine sheets on a common key.
    - **Analyze**: Summarize or Aggregate data.
    - **Edit**: Rename/Delete columns.

## Capabilities

### 1. Merge & Join (Across Sheets)
- **Sync Sheets**: `python ./scripts/excel_processor.py merge --input "file1.xlsx" --sheet "OldData" --input2 "file2.xlsx" --sheet2 "NewData" --key "ID"`
- **VLookup/Join**: `python ./scripts/excel_processor.py join --input "inventory.xlsx" --sheet "Items" --input2 "prices.xlsx" --sheet2 "PriceList" --key "SKU"`

### 2. Batch Cleaning (All Sheets)
- **Dedupe All**: `python ./scripts/excel_processor.py dedupe --input "data.xlsx" --sheet ALL --column "ID"`
- **Filter All**: `python ./scripts/excel_processor.py filter --input "logs.xlsx" --sheet ALL --column "Level" --value "Error"`

### 3. Analysis & Modification
- **Summary**: `python ./scripts/excel_processor.py summary --input "file.xlsx" --sheet ALL`
- **Drop Column**: `python ./scripts/excel_processor.py drop --input "file.xlsx" --sheet "Sheet1" --column "PrivateData"`

## Workflow Guidance
1. **Identify Target**: Ask the user which sheet(s) they want to work on if it's not clear.
2. **Execute**: Use `excel_processor.py` with the `--sheet` flag.
3. **Verify**: If multiple sheets are saved, inform the user they are all preserved in the output file.
