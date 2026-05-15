# Google Sheet Agent (Advanced Excel Assistant)

A powerful, interactive Gemini CLI agent designed to automate complex Excel and CSV tasks.

## 🚀 Features
- **Interactive Menu**: Run the agent and select from a list of common tasks.
- **Sync/Merge**: Update a new sheet with data from an old one using a unique key.
- **Batch Processing**: Apply cleaning or filtering rules to **all sheets** in a workbook at once.
- **VLookup/Join**: Combine multiple sheets into one using a common key.
- **Advanced Cleaning**: Deduplicate, filter, and sort data with ease.
- **Data Analysis**: Generate statistical summaries and aggregated (pivot) reports.

## 🛠️ Requirements
- [Gemini CLI](https://github.com/google/gemini-cli)
- Python 3.x
- `pandas` and `openpyxl` libraries

## 📥 Installation

1. **Clone or Download** this folder.
2. **Install Python dependencies**:
   ```bash
   pip install pandas openpyxl
   ```
3. **Install as an Extension**:
   Using HTTPS:
   ```bash
   gemini extensions install https://github.com/suraj8277/google-sheet-agent
   ```
   Using SSH (Recommended for authenticated users):
   ```bash
   gemini extensions install git@github.com:suraj8277/google-sheet-agent.git
   ```
4. **Reload Gemini**:
   ```bash
   /skills reload
   ```

## 📖 Usage
Simply tell Gemini what you want to do:
- *"Gemini, summarize all sheets in 'inventory.xlsx'."*
- *"Gemini, merge 'old_list.csv' into 'new_list.xlsx' using the 'Email' column."*
- *"Gemini, run the excel agent on 'data.xlsx'."*

## 🔒 Security Note
This tool is designed to work with **local files**. If you wish to use the Google Sheets API, you must provide your own `service_account.json` in the skill directory. **Never commit your private keys or credentials to GitHub.**
