import csv
import json
from typing import List, Dict

def csv_to_json(csv_file: str, json_file: str) -> None:
    """
    Convert a CSV file to JSON format.
    
    Args:
        csv_file (str): Path to the input CSV file
        json_file (str): Path to the output JSON file
    """
    try:
        # Read CSV file
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            data: List[Dict] = []
            
            # Convert each row to a dictionary
            for row in csv_reader:
                # Clean empty strings
                cleaned_row = {
                    key: value.strip() if value.strip() else None
                    for key, value in row.items()
                }
                data.append(cleaned_row)
        
        # Write to JSON file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
        print(f"Successfully converted {csv_file} to {json_file}")
        print(f"Total entries converted: {len(data)}")
            
    except FileNotFoundError:
        print(f"Error: Could not find the file {csv_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Usage
if __name__ == "__main__":
    input_file = "Test Verb Present tense.csv"
    output_file = "laz_verbs.json"
    csv_to_json(input_file, output_file)