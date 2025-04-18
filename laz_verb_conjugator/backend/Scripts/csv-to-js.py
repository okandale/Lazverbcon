#!/usr/bin/env python3
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from backend.data.convert import csv_to_json

def convert_csv_to_js(input_csv_path, output_js_path):
    """
    Convert CSV file containing verb data to an optimized JavaScript module.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_js_path (str): Path where the JavaScript file should be saved
    """
    try:
        # Read CSV file
        df = pd.read_csv(input_csv_path)
        
        # Extract required columns and remove any rows with missing values
        verb_data = df[['Laz Infinitive', 'Turkish Verb', 'English Translation']].dropna()
        
        # Convert to optimized format
        optimized_verbs = [
            {
                'l': row['Laz Infinitive'],
                't': row['Turkish Verb'],
                'e': row['English Translation']
            }
            for _, row in verb_data.iterrows()
        ]

        # Calculate sizes for logging
        original_size = len(json.dumps(verb_data.to_dict('records')))
        optimized_size = len(json.dumps(optimized_verbs))
        
        # Create JavaScript content with documentation
        js_content = f"""// Generated by csv-to-js-converter.py on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Original CSV: {Path(input_csv_path).name}
// Size optimization: {original_size:,} bytes → {optimized_size:,} bytes

// Optimized verb list with shortened property names:
// l: Laz Infinitive
// t: Turkish Verb
// e: English Translation
export const verbList = {json.dumps(optimized_verbs, indent=2, ensure_ascii=False)};

// Search function that handles all three languages
export const processVerbSearch = (searchTerm, verbs = verbList) => {{
  if (!searchTerm) return verbs;
  
  const searchLower = searchTerm.toLowerCase().trim();
  return verbs.filter(verb => 
    verb.l.toLowerCase().includes(searchLower) ||
    verb.t.toLowerCase().includes(searchLower) ||
    verb.e.toLowerCase().includes(searchLower)
  );
}};

// Format a verb for display (converts short keys to full names)
export const formatVerbForDisplay = (verb) => ({{
  'Laz Infinitive': verb.l,
  'Turkish Verb': verb.t,
  'English Translation': verb.e
}});

// Format the entire list for display
export const formatVerbListForDisplay = (verbs = verbList) => 
  verbs.map(formatVerbForDisplay);

// Get verb by Laz infinitive
export const getVerbByInfinitive = (infinitive) => 
  verbList.find(v => v.l.toLowerCase() === infinitive.toLowerCase());

// Function to check if a verb exists
export const verbExists = (infinitive) => 
  verbList.some(v => v.l.toLowerCase() === infinitive.toLowerCase());
"""

        # Write to file
        with open(output_js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"✅ Successfully converted {len(optimized_verbs)} verbs")
        print(f"📊 Size reduction: {original_size:,} → {optimized_size:,} bytes ({(1 - optimized_size/original_size)*100:.1f}% smaller)")
        print(f"📝 Output written to: {output_js_path}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find input CSV file: {input_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"❌ Error: The CSV file is empty: {input_csv_path}")
    except KeyError as e:
        print(f"❌ Error: Required column missing from CSV: {e}")
    except Exception as e:
        print(f"❌ Error: An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Assuming script is in the backend folder alongside the CSV
    script_dir = Path(__file__).parent.parent
    
    input_path = script_dir / "data" / "Test Verb Present tense.csv"
    output_path = script_dir.parent / "frontend" / "src" / "components" / "verb-data.js"
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    convert_csv_to_js(input_path, output_path)
    
    # Now, call convert
    base_path = Path(__file__).parent / ".." / "data"
    input_file = base_path / "Test Verb Present tense.csv"
    output_file = base_path / "verb_data.json"
    csv_to_json(input_file, output_file)