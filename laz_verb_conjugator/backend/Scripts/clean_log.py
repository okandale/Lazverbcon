import json
import os

# Dynamically determine the path relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'logs', 'request_response.log')  # Adjust folder name if necessary
output_file = os.path.join(script_dir, 'logs', 'cleaned_logs.json')

def clean_log_file(input_path, output_path):
    cleaned_data = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Extract the JSON part of the log line
                json_part = line.split(" - ", 1)[1]  # Split at " - " and take the JSON part
                log_entry = json.loads(json_part)
                
                # Extract request and response
                cleaned_entry = {
                    "request": log_entry.get("request"),
                    "response": log_entry.get("response")
                }
                cleaned_data.append(cleaned_entry)
            except (IndexError, json.JSONDecodeError):
                # Skip improperly formatted lines
                continue

    # Write cleaned data to output file in UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as output:
        json.dump(cleaned_data, output, indent=4, ensure_ascii=False)  # Use ensure_ascii=False for proper UTF-8

    print(f"Cleaned data written to {output_path}")

# Run the cleaning process
clean_log_file(input_file, output_file)
