---
name: google-sheet-agent
description: An advanced agent for processing local Excel and CSV files. Capabilities include multi-sheet support, merging, filtering, sorting, deduplication, data summaries, AI-powered smart queries, and automatic visualization.
---
# Advanced Excel Agent (v2.0 - Live Assistant Brain)

This skill enables a wide range of data processing and analysis tasks on local Excel (.xlsx) and CSV files, including full support for multi-sheet workbooks and proactive intelligent help.

## 🌟 Interactive Mode (Main Menu)
If the user is vague or asks to "run the agent", **ALWAYS** use `ask_user` to present these options:

- **Header**: "Action"
- **Question**: "What would you like to do with your spreadsheet(s)?"
- **Options**:
    - **Sync/Merge**: Update a sheet with data from another.
    - **Analyze (Smart)**: Ask a natural language question about the data.
    - **Visualize**: Generate charts (Bar, Pie, Line).
    - **Batch Process**: Apply a clean/filter rule to ALL sheets.
    - **Edit**: Rename/Delete columns.

## 🧠 Advanced Capabilities

### 1. Smart Query (Natural Language)
Instead of specific commands, you can now answer complex questions.
- **Workflow**: Translate the user's question into a Python pandas snippet and run it.
- **Command**: `python ./scripts/query_engine.py --input "file.xlsx" --code "result = df[df['Status'] == 'Active'].count()"`

### 2. Visual Brain (Charts)
Automatically generate images from data.
- **Command**: `python ./scripts/visualizer.py --input "data.xlsx" --type "pie" --x "Region" --output "region_dist.png"`

### 3. Multi-Sheet Operations
- **Specific Sheet**: Use `--sheet "SheetName"`.
- **All Sheets (Batch)**: Use `--sheet ALL`.

### 4. Merge & Join
- **Sync Sheets**: `python ./scripts/excel_processor.py merge --input "file1.xlsx" --sheet "OldData" --input2 "file2.xlsx" --sheet2 "NewData" --key "ID"`

### 5. Cleaning & Modification
- **Dedupe All**: `python ./scripts/excel_processor.py dedupe --input "data.xlsx" --sheet ALL --column "ID"`
- **Rename**: `python ./scripts/excel_processor.py rename --input "file.xlsx" --column "Old" --value "New"`

## 🤖 Live Assistant Workflow
1. **Proactive Check**: When a file is mentioned, offer a `summary` automatically.
2. **Context Awareness**: If a Jira ticket is mentioned alongside a sheet (e.g., "Check status of servers in this sheet based on SYS-123"), use `Smart Query` to filter the sheet for relevant hostnames.
3. **Verification**: Always confirm the output filename and location.
