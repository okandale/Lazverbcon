# the version with correct simple present tense SxOx conjugations and "d" preverb, but the preverb function needs to be tidied up.
# the version with correct simple present tense SxOx conjugations and "d" preverb..
# added optional preverb 'ko' - won't reflect in conjugator
# added compound words
import pandas as pd
import os
from utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    handle_special_case_coz,
    handle_special_case_gy,
    handle_special_case_u,
    subjects
)

# Load the CSV file
file_path = os.path.join('notebooks', 'data', 'Test Verb Present tense.csv')

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

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'cel', 'ce', 'do', 'ye'): {
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

# Phonetic rules for 'v' and 'g'
def get_phonetic_rules(region):
    if region == 'FA':
        phonetic_rules_v = {
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
            'b': ['l', 'a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
            'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
            'm': ['n']
        }
    else:
        phonetic_rules_v = {
            'v': ['a', 'e', 'i', 'o', 'u'],
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
            'b': ['l', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
            'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
            'm': ['n']
        }

    phonetic_rules_g = {
        'g': ['a', 'e', 'i', 'o', 'u'],
        'k': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
        'g': ['d', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
        'ǩ': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆']
    }

    return phonetic_rules_v

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# Function to conjugate present tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
# Function to conjugate present tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
def conjugate_present(infinitive, subject, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    
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

    # Get the first word from the infinitive at the start
    first_word_infinitive = get_first_word(infinitive)

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


            # Use the first word from the infinitive consistently
            first_word = first_word_infinitive

            subject_markers = {
                'S1_Singular': 'm',
                'S2_Singular': 'g',
                'S3_Singular': '',
                'S1_Plural': 'm',
                'S2_Plural': 'g',
                'S3_Plural': ''
            }
        
            suffixes = {
                'S1_Singular': '',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'an',
                'S2_Plural': 'an',
                'S3_Plural': 'an'
            }

            # Extract the preverb from the infinitive if it exists
            preverb = ''
            if main_infinitive != 'oǩoreʒxu':
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


            if preverb:
                preverb_form = preverbs_rules.get((preverb,), {}).get(subject, preverb)
            else:
                prefix = subject_markers[subject]

            # Specific case: preverb modifications based on subject
            preverb_form = ''

            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')):
                preverb = preverb[:-1] 

            if preverb in ('ge', 'e', 'ce'):
                if root.startswith('ca'):
                    if subject in ('S3_Singular', 'S3_Plural'):
                        preverb = 'c'
                    root = root[1:]
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'm'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'g'
                else:
                    prefix = preverb
            
            elif preverb == 'do':
                if subject in ('S3_Singular', 'S3_Plural') and not obj:
                    preverb = ''
                else:
                    root = root[2:] if region in ('PZ', 'AŞ', 'HO') else root[1:]
                
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
                if root == "diç̌irs":
                    root = 'ç̌irs'
                    if subject in ('S3_Singular', 'S3_Plural'):
                        if obj in ('O1_Singular', 'O1_Plural'):
                            adjusted_prefix = 'dova' if region in ('PZ', 'AŞ', 'HO') else 'doba'
                        else:
                            adjusted_prefix = "di"
                        prefix = adjusted_prefix
                    elif subject in ('S1_Singular', 'S1_Plural'):
                        adjusted_prefix = 'doma'
                        prefix = adjusted_prefix
                    elif subject in ('S2_Singular', 'S2_Plural'):
                        adjusted_prefix = 'doga'
                        prefix = adjusted_prefix
                    else:
                        prefix = subject_markers[subject]

                elif root == "dvaç̌irs":
                    root = 'ç̌irs'
                    if subject in ('S3_Singular', 'S3_Plural'):
                        if obj in ('O1_Singular', 'O1_Plural'):
                            adjusted_prefix = 'dova' if region in ('PZ', 'AŞ', 'HO') else 'doba'
                        else:
                            adjusted_prefix = "dva"
                        prefix = adjusted_prefix
                    elif subject in ('S1_Singular', 'S1_Plural'):
                        adjusted_prefix = 'doma'
                        prefix = adjusted_prefix
                    elif subject in ('S2_Singular', 'S2_Plural'):
                        adjusted_prefix = 'doga'
                        prefix = adjusted_prefix
                    else:
                        prefix = subject_markers[subject]


                elif subject in ('S3_Singular', 'S3_Plural') and obj in ('O1_Singular', 'O1_Plural'):
                    adjusted_prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                    if infinitive in ('olimbu', 'oropumu'):
                        prefix = '(go)' + adjusted_prefix
                    else:
                        prefix = adjusted_prefix
                elif subject in ('S1_Singular', 'S1_Plural') and obj in ('O3_Singular', 'O3_Plural'):
                    adjusted_prefix = 'm'
                    prefix = adjusted_prefix
                else:
                    prefix = subject_markers[subject]

            # Optional preverb handling
            if use_optional_preverb and not preverb:
                prefix = 'ko' + prefix
                if subject in ['O3_Singular', 'O3_Plural']:
                    prefix = 'k' + prefix



            suffix = suffixes[subject]
            if obj:
                if subject == 'S3_Singular' and obj == 'O3_Singular':
                    suffix = ''
                elif subject == 'S3_Singular' and obj == 'O3_Plural':
                    if root.endswith('rs'):
                        root = root[:-1]
                    suffix = 'an'
                elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                    if root.endswith(('en', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                elif subject in ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S3_Plural'] and obj in ['O1_Singular', 'O2_Singular']:
                    if root.endswith(('n', 'rs')):
                        root = root[:-1]
                    suffix = '' if infinitive.endswith('rs') else 'r'
                elif subject in ['S1_Singular', 'S1_Plural', 'S2_Singular', 'S2_Plural'] and obj in ('O1_Plural', 'O2_Plural'):
                    if root.endswith(('n', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                elif subject in ['S1_Plural', 'S2_Plural'] and obj in ('O1_Singular', 'O2_Singular'):
                    if root.endswith(('n', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                elif subject in ['S1_Singular', 'S2_Singular'] and obj in ['O3_Singular', 'O3_Plural']:
                    suffix = ''
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Singular'] and obj in ('O3_Singular', 'O3_Plural'):
                    if root.endswith('rs'):
                        root = root[:-1]
                    suffix = 'an'
                elif subject == 'S3_Plural':
                    if root.endswith('rs'):
                        root = root[:-1]
                    suffix = 'an'


            # Conjugate the verb
            # Conjugate the verb
            if preverb in ('go', 'gy', 'coz', 'd'):
                if suffix == 'r' and root.endswith('n'):
                    final_root = root
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root + 'r'
                else:
                    final_root = root
            else:
                if subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root
                else:
                    final_root = root

            conjugated_verb = f"{prefix}{final_root}{suffix}"




            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
        for region, conjugation_list in result.items():
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


# Define personal pronouns outside of regions
personal_pronouns_general = {
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
    'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
    'O3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe'
}
