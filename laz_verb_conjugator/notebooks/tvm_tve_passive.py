#!/usr/bin/env python
# coding: utf-8

# In[11]:


# passive form with present, past, future, past progressive tense
# update similarily to potential form if all forms stay the same.
import pandas as pd
import os

# Load the CSV file
file_path = os.path.join('notebooks', 'data', 'Test Verb Present tense.csv')

# Read the CSV file
df = pd.read_csv(file_path)

# Filter for 'TVE' and 'TVM' verbs
df_tve = df[df['Category'].isin(['TVE', 'TVM'])]

# Convert the dataframe to a dictionary
verbs = {}
regions = {}
for index, row in df_tve.iterrows():
    infinitive = row['Laz Infinitive']
    passive_forms = row[['Laz 3rd Person Singular Present', 'Laz 3rd Person Singular Present Alternative 1', 'Laz 3rd Person Singular Present Alternative 2']].dropna().tolist()
    region = row[['Region', 'Region Alternative 1', 'Region Alternative 2']].dropna().tolist()
    regions_list = []
    for reg in region:
        regions_list.extend([r.strip() for r in reg.split(',')])
    if not regions_list:
        regions_list = ["All"]
    verbs[infinitive] = list(zip(passive_forms, region))
    regions[infinitive] = regions_list

# Function to process compound verbs and return the latter part
def process_compound_verb(verb):
    root = ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb
    return root

# Function to get the first word of a compound verb
def get_first_word(verb):
    return verb.split()[0] if len(verb.split()) > 1 else ''

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'ok̆o', 'gama', 'mo'): {
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
        'S3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'S1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
        'S3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

def get_suffixes(tense, region, causative):
    suffixes = {}
    if tense == 'present':
        suffixes = {
            'S1_Singular': 'er',
            'S2_Singular': 'er',
            'S3_Singular': 'en',
            'S1_Plural': 'ert',
            'S2_Plural': 'ert',
            'S3_Plural': 'enan' 
        }
        if causative:
            suffixes.update({
                'S1_Singular': 'apiner',
                'S2_Singular': 'apiner',
                'S3_Singular': 'apinen',
                'S1_Plural': 'apinert',
                'S2_Plural': 'apinert',
                'S3_Plural': 'apinenan'
            })
    elif tense == 'future':
        suffixes = {
            'S1_Singular': 'are' if region == "PZ" else 'are' if region in ('AŞ', 'FA') else 'aminon',
            'S2_Singular': 'are' if region == "PZ" else 'are' if region in ('AŞ', 'FA') else 'aginon',
            'S3_Singular': 'asere' if region == "PZ" else 'asen' if region in ('AŞ', 'FA') else 'asinon',
            'S1_Plural': 'atere' if region == "PZ" else 'aten' if region in ('AŞ', 'FA') else 'aminonan',
            'S2_Plural': 'atere' if region == "PZ" else 'aten' if region in ('AŞ', 'FA') else 'aginonan',
            'S3_Plural': 'aneran' if region == "PZ" else 'anenan' if region in ('AŞ', 'FA') else 'asinonan'
        }
        if causative:
            suffixes.update({
                'S1_Singular': 'apaminon' if region == "HO" else 'apare',
                'S2_Singular': 'apaginon' if region == "HO" else 'apare',
                'S3_Singular': 'apasinon' if region == "HO" else 'apasere' if region == "PZ" else 'apasen',
                'S1_Plural': 'apaminonan' if region == "HO" else 'apaten' if region == "PZ" else 'apaten',
                'S2_Plural': 'apaginonan' if region == "HO" else 'apaten' if region == "PZ" else 'apaten',
                'S3_Plural': 'apasinonan' if region == "HO" else 'apaten' if region == "PZ" else 'apaten'
                })
    elif tense == 'past':
        suffixes = {
            'S1_Singular': 'i',
            'S2_Singular': 'i',
            'S3_Singular': 'u',
            'S1_Plural': 'it',
            'S2_Plural': 'it',
            'S3_Plural': 'ey' if region in ('AŞ') else 'es'
        }
        if causative:
            suffixes.update({
                'S1_Singular': 'apineri',
                'S2_Singular': 'apineri',
                'S3_Singular': 'apinenu',
                'S1_Plural': 'apinerit',
                'S2_Plural': 'apinerit',
                'S3_Plural': 'apinenanu'
                })
    elif tense == 'pastpro':
        suffixes = {
            'S1_Singular': 'ert̆i',
            'S2_Singular': 'ert̆i',
            'S3_Singular': 'ert̆u',
            'S1_Plural': 'ert̆it',
            'S2_Plural': 'ert̆it',
            'S3_Plural': 'ert̆es' 
        }
        if causative:
            suffixes.update({
                'S1_Singular': 'apinert̆i',
                'S2_Singular': 'apinert̆i',
                'S3_Singular': 'apinert̆u',
                'S1_Plural': 'apinert̆it',
                'S2_Plural': 'apinert̆it',
                'S3_Plural': 'apinent̆es'
                })
            
    return suffixes

def conjugate_passive_form(infinitive, tense, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    
    if applicative and causative:
        raise ValueError("A verb can either have an applicative marker or a causative marker, but not both.")
    if applicative and obj is None:
        raise ValueError("Applicative requires an object to be specified.")
    
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
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }

            suffixes = get_suffixes(tense, region, causative)

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
                root = 'i' + root[len(preverb):-1]  # Remove only the preverb
            elif root == "oşu":
                root = infinitive[1:-1] + "v"
            else:
                root = 'i' + root[1:-1]  # Remove the last character of the root

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)

            # Adjust the prefix based on the first letter for phonetic rules
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb != 'go':
                preverb = preverb[:-1]
            
            
            prefix = subject_markers[subject]
            
            if preverb == "me" and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                preverb = "n"
                prefix = preverb + subject_markers[subject]
            elif preverb in ('gama', 'gam'):
                root = 'iç'
                preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gamo'
                prefix = preverb + subject_markers[subject]
            elif preverb == 'go' and root.startswith(('a','e','i','o','u')) and subject not in ('S1_Singular', 'S1_Plural'):
                prefix = "gv" + subject_markers[subject] if region in ('HO', 'PZ', 'AŞ') else "g" + subject_markers[subject]
            elif preverb:
                # Adjust the prefix based on the first letter of the root
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    if root.startswith('n'):
                        root = root[1:]
                    prefix = preverb + 'm'
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix(subject_markers[subject], first_letter, phonetic_rules_v)
                    if root.startswith('n'):
                        root = root[1:]
                    prefix = preverb + adjusted_prefix
                else:
                    prefix = preverb + subject_markers[subject]
            else:
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    if root.startswith('n'):
                        root = root[1:]
                    prefix = 'm' + subject_markers[subject]
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix(prefix, first_letter, phonetic_rules_v)
                    prefix = adjusted_prefix
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
def collect_conjugations_all(infinitive, subjects, tense='present', obj=None, applicative=False, causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_passive_form(infinitive, tense, subject=subject, causative=causative)
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

# Define personal pronouns outside of regions
personal_pronouns_general = {
    'O3_Singular': 'heya',
    'O3_Plural': 'hentepe',
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O1_Plural': 'çku',
    'O2_Plural': 'tkva'
}

subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']


# Example usage
infinitive = 'ot̆axu'
tense = 'pastpro' # insert 'past', 'present', 'future' or 'past progressive'
causative = False # set to "True" or "False" - currently only implemented for present tense!
all_conjugations = collect_conjugations_all(infinitive, subjects, tense=tense, causative=causative)

# Print the formatted conjugations
print(f"All subject conjugations of infinitive '{infinitive}' ({tense} tense):")
print(format_conjugations(all_conjugations))



