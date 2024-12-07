import pandas as pd
import os

def excel_to_csv(input_file, output_file, use_bom=False):
    # Read the Excel file
    df = pd.read_excel(input_file, engine='openpyxl')
    
    # Write to CSV file with UTF-8 encoding
    encoding = 'utf-8-sig' if use_bom else 'utf-8'
    df.to_csv(output_file, index=False, encoding=encoding)

    print(f"Conversion complete. CSV file saved as {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = os.path.join('notebooks', 'data', 'Test Verb Present tense.xlsx')
    output_file = os.path.join('notebooks', 'data', 'Test Verb Present tense.csv')
    
    # Set use_bom=True to match the original function, or False to match Excel's "CSV (UTF-8)"
    excel_to_csv(input_file, output_file, use_bom=False)