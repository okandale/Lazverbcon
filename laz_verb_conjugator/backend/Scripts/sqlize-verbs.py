"""Read the .csv reference file and produce INSERT statements for the database."""
import os
import csv
from pathlib import Path

CATEGORIES_MAP = {
    "TVM": "NOMINATIVE",
    "TVE": "ERGATIVE",
    "IVD": "DATIVE"
}

def sqlize(input_csv_path, output_csv_path):
    with open(input_csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip the very first line (the headers)
        current_verb_id = 1
        for row in reader:
            (
                infinitive,
                category,
                laz_3rd_person_singular_present,
                region,
                laz_3rd_person_singular_present_alt1,
                region_alt1,
                laz_3rd_person_singular_present_alt2,
                region_alt2,
                english_translation,
                turkish_verb,
                *_
            ) = row
            print(
                f"INSERT INTO verb(verb_id, infinitive_form) VALUES({current_verb_id}, '{infinitive}');"
            )
            category = category.strip()
            
            verb_regions = map(lambda r: r.strip(), region.split(','))
            # Loop for the "base regions"
            for current_region in verb_regions:
                print(
                    "INSERT INTO region_verb(region_code, verb_id, verb_type, verb_root, english_translation, turkish_verb) "
                    f"VALUES('{current_region}', {current_verb_id}, '{CATEGORIES_MAP[category]}', '{laz_3rd_person_singular_present}', '{english_translation}', '{turkish_verb}');"
                )            
            # And handle "alterative" forms.
            if region_alt1:
                print(
                    "INSERT INTO region_verb(region_code, verb_id, verb_type, verb_root, english_translation, turkish_verb) "
                    f"VALUES('{region_alt1}', {current_verb_id}, '{CATEGORIES_MAP[category]}', '{laz_3rd_person_singular_present_alt1}', '{english_translation}', '{turkish_verb}');"
                )
            
            if region_alt2:
                print(
                    "INSERT INTO region_verb(region_code, verb_id, verb_type, verb_root, english_translation, turkish_verb) "
                    f"VALUES('{region_alt2}', {current_verb_id}, '{CATEGORIES_MAP[category]}', '{laz_3rd_person_singular_present_alt2}', '{english_translation}', '{turkish_verb}');"
                )
                
            
            current_verb_id += 1
    
if __name__ == "__main__":
    base_path = Path(__file__).parent / ".." / "data"
    input_file = base_path / "Test Verb Present tense.csv"
    output_file = base_path / "schema.sql"
    sqlize(input_file, output_file)