#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os

# Load the CSV file
file_path = os.path.join('notebooks', 'data', 'Test Verb Present tense.csv')

from notebooks.my_functions import get_personal_pronouns_ivd
# Read the CSV file.
df = pd.read_csv(file_path)

# Now continue with your original processing logic

# Filter for 'IVD' verbs (if you have already added the 'Category' column)
df_ivd = df[df['Category'] == 'IVD']

# Convert the filtered dataframe to a dictionary
verbs = {}
regions = {}
for index, row in df_ivd.iterrows():
    infinitive = row['Laz Infinitive']
    present_forms = row[['Laz 3rd Person Singular Present', 'Laz 3rd Person Singular Present Alternative 1', 'Laz 3rd Person Singular Present Alternative 2']].dropna().tolist()
    region = row[['Region', 'Region Alternative 1', 'Region Alternative 2']].dropna().tolist()
    regions_list = []
    for reg in region:
        regions_list.extend([r.strip() for r in reg.split(',')])
    if not regions_list:
        regions_list = ["All"]
    verbs[infinitive] = list(zip(present_forms, region))
    regions[infinitive] = regions_list

# Function to process compound verbs and return the latter part
def process_compound_verb(verb):
    return ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'ce', 'd', 'ye'): {
        'S1_Singular': 'om',
        'S2_Singular': 'og',
        'S3_Singular': '',
        'S1_Plural': 'om',
        'S2_Plural': 'og',
        'S3_Plural': ''
    },
    ('go',): {
        'S1_Singular': 'gom',
        'S2_Singular': 'gog',
        'S3_Singular': 'go',
        'S1_Plural': 'gom',
        'S2_Plural': 'gog',
        'S3_Plural': 'go'
    },
    ('gy',): {
        'S1_Singular': 'gem',
        'S2_Singular': 'geg',
        'S3_Singular': 'gyo',
        'S1_Plural': 'gem',
        'S2_Plural': 'geg',
        'S3_Plural': 'gyo'
    },
    ('coz',): {
        'S1_Singular': 'cem',
        'S2_Singular': 'ceg',
        'S3_Singular': 'coz',
        'S1_Plural': 'cem',
        'S2_Plural': 'ceg',
        'S3_Plural': 'coz'
    }
}

# Function to handle special letters
def get_first_letter(root):
    if len(root) > 1 and root[:2] in ['t̆', 'ç̌', 'k̆', 'p̌']:
        return root[:2]
    return root[0]

# Function to handle special letters
def get_first_vowel_index(word):
    vowels = "aeiou"
    for index, char in enumerate(word):
        if char in vowels:
            return index
    return -1

# Function to handle the specific case for verbs starting with 'u' and verbs with 'i' in the root
def handle_special_case_u(root, subject, preverb):
    if root.startswith('u'):
        if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
            root = 'i' + root[1:]

    if preverb == 'd':
        first_vowel_index = get_first_vowel_index(root)
        if first_vowel_index != -1 and root[first_vowel_index] == 'i':
            if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                root = root[:first_vowel_index] + 'a' + root[first_vowel_index + 1:]
        else:
            root = root

    return root

# Function to handle special case for 'gy' preverb
def handle_special_case_gy(root, subject):
    if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
        root = root[0] + root[1:]
    return root

# Function to handle special case for 'coz' preverb
def handle_special_case_coz(root, subject):
    return 'ozun'

# Function to remove the first character for certain roots
def remove_first_character(root):
    return root[1:]

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else 'hiyas',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'S1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# Function to conjugate past tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
def conjugate_past(infinitive, subject, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    
    if applicative and causative:
        raise ValueError("A verb can either have an applicative marker or a causative marker, but not both.")
    if applicative and obj is None:
        raise ValueError("Applicative requires an object to be specified.")
    if causative and obj is None:
        raise ValueError("Causative requires an object to be specified.")
    
    if infinitive not in verbs:
        return {region: [(subject, obj, f"Infinitive {infinitive} not found.")] for region in regions[infinitive]}

    # Get the regions for the current infinitive
    regions_list = regions[infinitive]

    main_infinitive = process_compound_verb(infinitive)
    # Get the third-person forms and their associated regions
    third_person_forms = verbs[infinitive]
    
    # Initialize region_conjugations
    region_conjugations = {region: [] for region in regions_list}

    # Process each third-person form and its associated regions
    for third_person, region_str in third_person_forms:
        regions_for_form = region_str.split(',')
        for region in regions_for_form:
            region = region.strip()
            personal_pronouns = get_personal_pronouns(region)
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)

            subject_markers = {
                'S1_Singular': 'm',
                'S2_Singular': 'g',
                'S3_Singular': '',
                'S1_Plural': 'm',
                'S2_Plural': 'g',
                'S3_Plural': ''
            }
        
            suffixes = {
                'S1_Singular': 'u',
                'S2_Singular': 'u',
                'S3_Singular': 'u',
                'S1_Plural': 'es',
                'S2_Plural': 'es',
                'S3_Plural': 'es'
            }
        
            object_prefixes = {
                'O1_Singular': 'm',
                'O1_Plural': 'm',
                'O2_Singular': 'g',
                'O2_Plural': 'g',
                'O3_Singular': '',
                'O3_Plural': ''
            }

            # Extract the preverb from the infinitive if it exists
            preverb = ''
            for pv_group in preverbs_rules.keys():
                if isinstance(pv_group, tuple):
                    for pv in pv_group:
                        if main_infinitive.startswith(pv):
                            preverb = pv
                            break
                elif main_infinitive.startswith(pv_group):
                    preverb = pv_group
                if preverb:
                    break

            # Process the compound root to get the main part
            root = process_compound_verb(third_person)

            # Remove the preverb from the third-person form if it exists
            if preverb and root.startswith(preverb):
                root = root[len(preverb):]

            # Handle special case for verbs starting with 'u' and 'i'
            root = handle_special_case_u(root, subject, preverb)

            # Handle special case for gy preverb
            if preverb == 'gy':
                root = handle_special_case_gy(root, subject)
            
            # Handle special case for coz preverb
            if preverb == 'coz':
                root = handle_special_case_coz(root, subject)


            # Adjust the prefix based on the preverb and subject
            first_letter = get_first_letter(root)
            adjusted_prefix = ''
            # Conjugate the verb
            preverb_form = preverb # Default to preverb itself if no specific rule is found
            if preverb:
                preverb_form = preverbs_rules.get((preverb,), {}).get(subject, preverb)
            else:
                prefix = subject_markers[subject]

            # Specific case: preverb modifications based on subject
            if preverb in ('ge', 'e', 'ce'):
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'om'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'og'
                else:
                    prefix = preverb
            
            elif preverb == 'd':
                if subject in ('S3_Singular', 'S3_Plural') and not obj:
                    preverb = 'd'
                    root = root[1:]
                else:
                    preverb = 'do'
                    if root.startswith('v'):
                        if region in ('PZ', 'AŞ', 'HO'):
                            root = root[1:]
                    else:
                        root = root
                
                if subject in ('S3_Singular', 'S3_Plural'):
                    if obj in ('O1_Singular', 'O1_Plural'):
                        adjusted_prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                        prefix = preverb + adjusted_prefix
                    else:
                        prefix = 'd' if region in ('FA') else 'dv'
                elif subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'm'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'g'
                else:
                    prefix = preverb[:-1]

            elif preverb == 'go':
                if subject in ('S3_Singular', 'S3_Plural') and not obj:
                    preverb = ''
                else:
                    root = root[2:] if region in ('PZ', 'AŞ', 'HO') else root[1:]
                
                if subject in ('S3_Singular', 'S3_Plural'):
                    if obj in ('O1_Singular', 'O1_Plural'):
                        adjusted_prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                        prefix = preverb + adjusted_prefix
                    else:
                        prefix = 'g' if region in ('FA') else 'gv'
                elif subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'm'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'g'
                else:
                    prefix = preverb[:-1]

            elif preverb == 'gy':
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb[:1] + 'em'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb[:1] + 'eg'
                else:
                    prefix = preverb[:1] + 'y'

            elif preverb == 'coz':
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = 'cem'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = 'ceg'
                else:
                    prefix = 'c'
            else:
                prefix = preverb_form

            # Additional prefix adjustments based on subject and object
            if not preverb:
                if subject in ('S3_Singular', 'S3_Plural') and obj in ('O1_Singular', 'O1_Plural'):
                    adjusted_prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                    if infinitive in ('olimbu', 'oropumu'):
                        prefix = '(go)' + adjusted_prefix
                    else:
                        prefix = adjusted_prefix
                else:
                    prefix = subject_markers[subject]

            # Optional preverb handling
            if use_optional_preverb and not preverb:
                prefix = 'ko' + prefix
                if subject in ['O3_Singular', 'O3_Plural']:
                    prefix = 'k' + prefix



            suffix = suffixes[subject]
            if root.endswith('en'):
                root = root[:-2]
            if root.endswith('s'):
                root = root[:-1]            
            if obj:
                if root.endswith('s'):
                    root = root[:-1] 
                if root.endswith('en'):
                    root = root[:-2]
                if subject == 'S3_Singular' and obj == 'O3_Singular':
                    suffix = suffixes[subject]
                elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                    suffix = 'it'
                elif subject in ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S3_Plural'] and obj in ['O1_Singular', 'O2_Singular']:
                    suffix = 'i'
                elif subject in ['S1_Singular', 'S1_Plural', 'S2_Singular', 'S2_Plural', 'S3_Plural'] and obj in ('O1_Plural', 'O2_Plural'):
                    suffix = 'it'
                elif subject in ['S1_Plural', 'S2_Plural'] and obj in ('O1_Singular', 'O2_Singular'):
                    suffix = 'it'
                elif subject in ['S1_Singular', 'S2_Singular'] and obj in ['O3_Singular', 'O3_Plural']:
                    suffix = 'u'
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Plural', 'S3_Singular'] and obj in ('O3_Singular', 'O3_Plural'):
                    suffix = 'ey' if region in ('AŞ') else 'es'
                else:
                    suffix = suffixes[subject]

                final_root = root

            # Conjugate the verb
            # Conjugate the verb
            if preverb in ('go', 'gy', 'coz', 'd'):
                if suffix == 'r' and root.endswith('n'):
                    final_root = root[:-1]
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root[:-1]
                else:
                    final_root = root
            else:
                if subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root[:-1]
                else:
                    final_root = root

            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_past(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations

# Define the function to format the output with region-specific pronouns
def format_conjugations(all_conjugations):
    result = []
    for region, conjugations in all_conjugations.items():
        personal_pronouns = get_personal_pronouns(region)
        result.append(f"{region}:")
        for subject, obj, conjugation in sorted(conjugations, key=lambda x: subjects.index(x[0])):
            subject_pronoun = personal_pronouns[subject]
            object_pronoun = personal_pronouns.get(obj, '')
            result.append(f"{subject_pronoun} {object_pronoun} {conjugation}")
    return '\n'.join(result)

def collect_conjugations_all_subjects_all_objects(infinitive, applicative=False, causative=False, use_optional_preverb=False):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']
    all_conjugations = {}
    for subject in subjects:
        for obj in objects:
            result = conjugate_past(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
            for region, conjugation_list in result.items():
                if region not in all_conjugations:
                    all_conjugations[region] = set()
                for conjugation in conjugation_list:
                    all_conjugations[region].add((subject, obj, conjugation[2]))
    return all_conjugations
def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, use_optional_preverb=False):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    return collect_conjugations(infinitive, subjects, obj, applicative, causative, use_optional_preverb)


# Define personal pronouns outside of regions
personal_pronouns_general = {
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
    'O1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
    'O3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe'
}

subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']


# Function to get the first word of a compound verb
def get_first_word(verb):
    return verb.split()[0] if len(verb.split()) > 1 else ''












