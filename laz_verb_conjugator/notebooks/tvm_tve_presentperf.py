#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Present Perfect
import pandas as pd
import os

# Load the CSV file
file_path = os.path.join('notebooks', 'data', 'Test Verb Present tense.csv')

# Read the CSV file.
df = pd.read_csv(file_path)

# Filter for 'TVE' and 'TVM' verbs
df_tve = df[df['Category'].isin(['TVE', 'TVM'])]

# Convert the dataframe to a dictionary
verbs = {}
regions = {}
for index, row in df_tve.iterrows():
    infinitive = row['Laz Infinitive']
    present_perfect_forms = row[['Laz 3rd Person Singular Present', 'Laz 3rd Person Singular Present Alternative 1', 'Laz 3rd Person Singular Present Alternative 2']].dropna().tolist()
    region = row[['Region', 'Region Alternative 1', 'Region Alternative 2']].dropna().tolist()
    regions_list = []
    for reg in region:
        regions_list.extend([r.strip() for r in reg.split(',')])
    if not regions_list:
        regions_list = ["All"]
    verbs[infinitive] = list(zip(present_perfect_forms, regions_list))
    regions[infinitive] = regions_list

# Function to process compound verbs and return the latter part
def process_compound_verb(verb):
    root = ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb
    return root

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'ok̆o', 'gama', 'mo', 'ye'): {
        'S1_Singular': 'v',
        'S2_Singular': '',
        'S3_Singular': '',
        'S1_Plural': 'v',
        'S2_Plural': '',
        'S3_Plural': ''
    }
}

# Phonetic rules for 'v' and 'g'
def get_phonetic_rules(region):
    if region == 'FA':
        phonetic_rules_v = {
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
            'b': ['a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
            'p̌': ['ç̌', 'k̆', 'q', 'ʒ̆', 't̆'],
            'm': ['n']
        }
    else:
        phonetic_rules_v = {
            'v': ['a', 'e', 'i', 'o', 'u'],
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
            'b': ['d', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
            'p̌': ['ç̌', 'k̆', 'q', 'ʒ̆', 't̆'],
            'm': ['n']
        }

    phonetic_rules_g = {
        'g': ['a', 'e', 'i', 'o', 'u'],
        'k': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
        'g': ['d', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
        'k̆': ['ç̌', 'k̆', 'q', 'ʒ̆', 't̆']
    }

    return phonetic_rules_v, phonetic_rules_g

# Function to adjust the prefix based on the first letter of the root
def adjust_prefix(prefix, first_letter, phonetic_rules):
    for p, letters in phonetic_rules.items():
        if first_letter in letters:
            return p
    return prefix

# Function to handle special letters
def get_first_letter(root):
    if len(root) > 1 and root[:2] in ['t̆', 'ç̌', 'k̆', 'p̌', 'ʒ̆']:
        return root[:2]
    elif root.startswith('gyoç̌k̆ams'):   # to skip the "gy" part.
        return root[2:]
    return root[0]

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyak' if region == "FA" else 'himuk' if region in ('AŞ', 'PZ') else 'hiyak',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'S1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
        'S3_Plural': 'hentepek' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

def get_suffixes(region):
    suffixes = {
        'S1_Singular': 'un' if region in ('FA', 'HO') else 'apun',
        'S2_Singular': 'un' if region in ('FA', 'HO') else 'apun', 
        'S3_Singular': 'un' if region in ('FA', 'HO') else 'apun',
        'S1_Plural': 'unan' if region in ('FA', 'HO') else 'apunan' if region == 'AŞ' else 'apuran',
        'S2_Plural': 'unan' if region in ('FA', 'HO') else 'apunan' if region == 'AŞ' else 'apuran',
        'S3_Plural': 'unan' if region in ('FA', 'HO') else 'apunan' if region == 'AŞ' else 'apuran'
    }
    return suffixes

def conjugate_present_perfect_form(infinitive, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):
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
    # Use the infinitive for the third-person forms
    third_person_forms = [(infinitive, ', '.join(regions_list))]
    
    # Initialize region_conjugations
    region_conjugations = {region: [] for region in regions_list}

    # Process each third-person form and its associated regions
    for third_person, region_str in third_person_forms:
        regions_for_form = region_str.split(',')
        for region in regions_for_form:
            region = region.strip()
            personal_pronouns = get_personal_pronouns(region)
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            
            # Set root to infinitive
            root = infinitive
            first_word = get_first_word(root)
            root = process_compound_verb(root)

            subject_markers = {
                'S1_Singular': 'mi',
                'S2_Singular': 'gi',
                'S3_Singular': 'i',
                'S1_Plural': 'mi',
                'S2_Plural': 'gi',
                'S3_Plural': 'i'
            }

            suffixes = get_suffixes(region)

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
                
            # Remove the preverb from the third-person form if it exists and add special rules for exceptions
            if preverb and root.startswith(preverb):
                root = root[len(preverb):-1]  # Remove only the preverb
            elif root in (('oşu', 'dodumu', 'otku')):
                root = infinitive[1:-1] + "v"
            else:
                root = root[1:-1]  # Remove the last character of the root

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)

            # Adjust the prefix based on the first letter for phonetic rules
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and infinitive != 'geç̌k̆u':
                preverb = preverb[:-1]
            if preverb == "me" and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                preverb = "n"
                prefix = preverb + subject_markers[subject]
            elif preverb in ('gama', 'gam'):
                root = 'ç'
                preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gamo'
                prefix = preverb + subject_markers[subject]
            elif preverb == 'go' and subject in ('S3_Singular', 'S3_Plural'):
                prefix = "gv" + subject_markers[subject] if region in ('HO') else "g" + subject_markers[subject]
            elif preverb == 'e' and subject in ('S3_Singular', 'S3_Plural'):
                prefix = "y" + subject_markers[subject]
            elif preverb:
                prefix = preverb + subject_markers[subject]
            else:
                prefix = subject_markers[subject]
       
            # Determine the suffix
            suffix = suffixes[subject]

            # Determine the final root to use
            final_root = root
            
            # Conjugate the verb
            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))  # Re-attach the first word of the compound verb

    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, mood=None):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_present_perfect_form(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add(conjugation)
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


# Example usage
infinitive = 'gamaçamu'
all_conjugations = collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, mood=None)

# Print the formatted conjugations
print(f"All subject conjugations of infinitive '{infinitive}' (present perfect tense):")
print(format_conjugations(all_conjugations))





