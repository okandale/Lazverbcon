import requests
import pandas as pd
import os
from utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    subjects
)
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
    potential_forms = row[['Laz 3rd Person Singular Present', 'Laz 3rd Person Singular Present Alternative 1', 'Laz 3rd Person Singular Present Alternative 2']].dropna().tolist()
    region = row[['Region', 'Region Alternative 1', 'Region Alternative 2']].dropna().tolist()
    regions_list = []
    for reg in region:
        regions_list.extend([r.strip() for r in reg.split(',')])
    if not regions_list:
        regions_list = ["All"]
    verbs[infinitive] = list(zip(potential_forms, region))
    regions[infinitive] = regions_list

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye'): {
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
            'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
            'm': ['n']
        }
    else:
        phonetic_rules_v = {
            'v': ['a', 'e', 'i', 'o', 'u'],
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
            'b': ['d', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
            'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
            'm': ['n']
        }

    phonetic_rules_g = {
        'g': ['a', 'e', 'i', 'o', 'u'],
        'k': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
        'g': ['d', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
        'ǩ': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆']
    }

    return phonetic_rules_v, phonetic_rules_g

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else '(h)emus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

def get_suffixes(tense, region):
    suffixes = {}
    if tense == 'present':
        suffixes = {
            'S1_Singular': 'en',
            'S2_Singular': 'en',
            'S3_Singular': 'en',
            'S1_Plural': 'enan',
            'S2_Plural': 'enan',
            'S3_Plural': 'enan'
        }
    elif tense == 'future':
        suffixes = {
            'S1_Singular': 'asere' if region == "PZ" else 'asen' if region in ('AŞ', 'FA') else 'asinon',
            'S2_Singular': 'asere' if region == "PZ" else 'asen' if region in ('AŞ', 'FA') else 'asinon',
            'S3_Singular': 'asere' if region == "PZ" else 'asen' if region in ('AŞ', 'FA') else 'asinon',
            'S1_Plural': 'anere' if region == "PZ" else 'anen' if region in ('AŞ', 'FA') else 'asinonan',
            'S2_Plural': 'anere' if region == "PZ" else 'anen' if region in ('AŞ', 'FA') else 'asinonan',
            'S3_Plural': 'anere' if region == "PZ" else 'anen' if region in ('AŞ', 'FA') else 'asinonan'
        }
    elif tense == 'past':
        suffixes = {
            'S1_Singular': 'u',
            'S2_Singular': 'u',
            'S3_Singular': 'u',
            'S1_Plural': 'es',
            'S2_Plural': 'es',
            'S3_Plural': 'es'
        }
    elif tense == 'pastpro':
        suffixes = {
            'S1_Singular': 'ert̆u',
            'S2_Singular': 'ert̆u',
            'S3_Singular': 'ert̆u',
            'S1_Plural': 'ert̆es',
            'S2_Plural': 'ert̆es',
            'S3_Plural': 'ert̆es'
        }
    elif tense == 'optative':
        suffixes = {
            'S1_Singular': 'as',
            'S2_Singular': 'as',
            'S3_Singular': 'as',
            'S1_Plural': 'an',
            'S2_Plural': 'an',
            'S3_Plural': 'an'
        }
    return suffixes

def conjugate_potential_form(infinitive, tense, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):
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
                'S1_Singular': 'ma',
                'S2_Singular': 'ga',
                'S3_Singular': 'a',
                'S1_Plural': 'ma',
                'S2_Plural': 'ga',
                'S3_Plural': 'a'
            }

            suffixes = get_suffixes(tense, region)

            if root == 'geçamu':
                root = 'geçu'

            if root == 'ceçamu':
                root == 'ceçu'

            # Extract the preverb from the infinitive if it exists
            preverb = ''
            preverb_exceptions = {'oǩoreʒxu'}  # Ensure this set is defined appropriately, add additionally to 256

            # Check if the infinitive is NOT in the exception list before extracting preverbs
            if infinitive not in preverb_exceptions:
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
            if preverb.endswith(('a','e','i','o','u')) and subject in subject_markers and subject_markers[subject].startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and subject in subject_markers and subject_markers[subject].startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular'):
                if preverb == 'ge':
                    preverb = preverb[:-1] + 'y' # for verbs that change to 'gy' in 2nd/3rd person
                elif preverb == 'ce':
                    preverb = preverb[:-1]
                else:
                    preverb = preverb # changed this for gonǯǩu 
              

            first_letter = get_first_letter(root)

            

            if preverb == "me" and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                preverb = "n"
                prefix = preverb + subject_markers[subject]
            elif preverb in ('gama', 'gam'):
                root = 'ç'
                if region in ('PZ', 'AŞ'):
                    preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gamo'
                else:
                    preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gama'
                prefix = preverb + subject_markers[subject]
            elif preverb == 'do' and subject_markers[subject].startswith(('a','e','i','o','u')):
                prefix = "dv" + subject_markers[subject] if region in ('HO', 'PZ', 'AŞ') else "d" + subject_markers[subject]
            elif preverb == 'go' and subject_markers[subject].startswith(('a','e','i','o','u')):
                prefix = "gv" + subject_markers[subject] if region in ('HO', 'PZ', 'AŞ') else "g" + subject_markers[subject]
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
def collect_conjugations_all(infinitive, subjects, tense='present', obj=None, applicative=False, causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_potential_form(infinitive, tense, subject=subject)
        for region, conjugation_list in result.items():
            if not region:
                continue
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations

def collect_conjugations_all_subjects_all_objects(infinitive, applicative=False, causative=False, use_optional_preverb=False):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']
    all_conjugations = {}
    for subject in subjects:
        for obj in objects:
            result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
            for region, conjugation_list in result.items():
                if region not in all_conjugations:
                    all_conjugations[region] = set()
                for conjugation in conjugation_list:
                    all_conjugations[region].add((subject, obj, conjugation[2]))
    return all_conjugations
def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, use_optional_preverb=False):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    return collect_conjugations(infinitive, subjects, obj, applicative, causative, use_optional_preverb)