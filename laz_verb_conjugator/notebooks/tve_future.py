#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Future tense
# Most up-to-date formula with preverbs (ge [along with geç̌k̆u's exception), e, ce, dolo, do [along with 'doguru'], go, oxo (based on oxoʒ̆onu) me (as actual preverb i.e. 'meçamu' not additional), applicative and object conjugation (and Ardeşen rule), now including causative marke. 
# directives ("me", "mo", "n") for non-preverb verbs are missing (i.e. oç̌aru - megiç̌aram)
# added "n" root changer - gomʒ̆am (gonʒ̆alu)
# added optional preverb 'me' and 'ko' - won't show up in conjugator
# added preverb 'gama'
import pandas as pd
import os

# Load the excel file
file_path = os.path.join('notebooks', 'data', 'Test Verb Present tense.xlsx')

# Read the excel file.
df = pd.read_excel(file_path)

# Filter for 'TVE' verbs --- Transitive Verbs Ergative
df_tve = df[df['Category'] == 'TVE']

# Convert the dataframe to a dictionary
verbs = {}
regions = {}
for index, row in df_tve.iterrows():
    infinitive = row['Laz Infinitive']
    future_forms = row[['Laz 3rd Person Singular Present', 'Laz 3rd Person Singular Present Alternative 1', 'Laz 3rd Person Singular Present Alternative 2']].dropna().tolist()
    region = row[['Region', 'Region Alternative 1', 'Region Alternative 2']].dropna().tolist()
    regions_list = []
    for reg in region:
        regions_list.extend([r.strip() for r in reg.split(',')])
    if not regions_list:
        regions_list = ["All"]
    verbs[infinitive] = list(zip(future_forms, region))
    regions[infinitive] = regions_list


# Function to process compound verbs and return the latter part
def process_compound_verb(verb):
    return ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb

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

# Function to determine the correct marker (applicative or causative)
def determine_marker(subject, obj, marker_type):
    if marker_type == 'applicative':
        if (subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural', 'S3_Singular', 'S3_Plural'] and obj in ['O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural']) or \
           (obj in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'] and subject in ['O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural', 'S3_Singular', 'S3_Plural']):
            return 'i'
        elif 'O3' in obj:
            return 'u'
        else:
            return ''
    elif marker_type == 'causative':
        return 'o'
    elif marker_type == 'causative and applicative':
        if (subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural', 'S3_Singular', 'S3_Plural'] and obj in ['O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural']) or \
           (obj in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'] and subject in ['O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural', 'S3_Singular', 'S3_Plural']):
            return 'i'
        elif 'O3' in obj:
            return 'u'
    return ''

# Function to handle marker and special case for verbs starting with 'i' or 'o'
def handle_marker(infinitive, root, marker):
    if infinitive == 'doguru':
        root = root[1:]  # Remove the first character 'd' from the root
    if infinitive in ('oç̌k̆omu', 'oşk̆omu') and marker == 'o':
        root = 'çams'
        marker = ''
    elif infinitive in ('oç̌k̆omu') and marker in ('i, u'):
        root = 'ç̌k̆omums'
    if infinitive == 'geç̌k̆u' and len(root) > 2: #special case for geç̌k̆u.
        if root[2] in ['i', 'o']:
            if marker in ['i', 'o']:
                root = root[:2] + marker + root[3:]  # Replace the third character 'i' or 'o' with 'i' or 'o'
            elif marker == 'u':
                root = root[:2] + 'u' + root[3:]  # Replace the third character 'i' or 'o' with 'u'
    elif root.startswith(('i', 'u', 'o')):
        if marker in ['i', 'o', 'u']:
            root = marker + root[1:]  # Replace the first 'i' or 'o' with 'i' or 'o'
        elif marker == 'u': # may be redundant now
            root = 'u' + root[1:]  # Replace the first 'i' or 'o' with 'u'
    else:
        root = marker + root
    return root

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyak' if region == "FA" else 'himuk' if region in ('AŞ', 'PZ') else 'hiyak',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'S1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
        'S3_Plural': 'hentepek' if region == "FA" else 'hinik' if region in ('AŞ', 'PZ') else 'entepek',
        'O3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çkin',
        'O2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva'
    }


# Update the conjugate_future function to return a dictionary
def conjugate_future(infinitive, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):
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



    
    # Process each third-person form and its associated regions
    for third_person, region_str in third_person_forms:
        regions_for_form = region_str.split(',')
        for region in regions_for_form:
            region = region.strip()
            personal_pronouns = get_personal_pronouns(region)
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)

            subject_markers = {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }

            suffixes = {
                'S1_Singular': 'aminon' if region == "HO" else 'are',
                'S2_Singular': 'aginon' if region == "HO" else 'are',
                'S3_Singular': 'asunon' if region == "HO" else 'asere' if region in ('PZ') else 'asen',
                'S1_Plural': 'aminonan' if region == "HO" else 'atere' if region in ('PZ') else 'aten',
                'S2_Plural': 'aginonan' if region == "HO" else 'atere' if region in ('PZ') else 'aten',
                'S3_Plural': 'asunonan' if region == "HO" else 'anere' if region in ('PZ') else 'anen'
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

            if root in ('imxors', 'ipxors') and infinitive == 'oç̌k̆omu':
                root = 'ç̌k̆omums'
            elif root in ('imxors') and infinitive == 'oşk̆omu':
                root = 'şk̆omums'
                
            # Remove the preverb from the third-person form if it exists
            if preverb and root.startswith(preverb):
                root = root[len(preverb):]

            # Determine the marker (applicative or causative)
            marker = ''
            marker_type = ''
            if applicative:
                marker = determine_marker(subject, obj, 'applicative')
                marker_type = 'applicative'
            elif causative:
                marker = determine_marker(subject, obj, 'causative')
                marker_type = 'causative'
            elif infinitive == 'oxoʒ̆onu' and (subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural']):
                marker = 'o'  # Default to 'o' for oxoʒ̆onu if neither applicative nor causative

            if infinitive == 'oxenu' and marker in ('u', 'i', 'o'):  # marker case for oxenu
                root = 'xenums'
            
            # Handle special case for verbs starting with 'i' or 'o'
            root = handle_marker(main_infinitive, root, marker)

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)

            # Special handling for "me"
            if preverb.endswith(('a','e','i','o','u')) and marker.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and main_infinitive != 'geç̌k̆u':
                preverb = preverb[:-1]
            if preverb == 'me' or (use_optional_preverb and not preverb):
                prefix = 'me'  # Default assignment for prefix
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'me' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'me' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = 'mom'
                else:
                    if preverb == 'me' and root.startswith(('a', 'e', 'i', 'o', 'u')):
                        preverb = 'n'
                        prefix = 'n'
                    else:
                        prefix = 'me'

            if use_optional_preverb and not preverb:
                prefix = 'ko' + prefix
                if subject in ['O3_Singular', 'O3_Plural']:
                    prefix = 'k'
            
            # Special handling for "do"
            elif preverb == 'do':
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'do' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'do' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = 'dom'
                elif marker_type == 'causative' or main_infinitive == 'doguru':  # to prevent double 'o's in causative form and S1O3 conjugations for doguru
                    prefix = 'd'
                else:
                    prefix = 'do'

            # Special handling for "geç̌k̆u"
            elif preverb == 'ge' and main_infinitive == 'geç̌k̆u':
                if marker:
                    root = root[2:]
                else:
                    root = root[2:]
                first_letter = get_first_letter(root)
                if marker_type in ('applicative', 'causative') and root.startswith(('a','i','e','o','u')):
                    prefix = 'gy'
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'ge' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'ge' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = 'gem'
                else:
                    prefix = 'gy'

           # Special handling for "ceç̌alu"
            elif preverb == 'ce' and main_infinitive == 'ceç̌alu':
                if marker:
                    root = root[2:]
                else:
                    root = root[1:]
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'ce' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'ce' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = 'cem'
                elif marker_type == 'causative':
                    prefix = 'ce'
                else:
                    prefix = 'c'

            # Special handling for "oxo"
            elif preverb == 'oxo':
                if marker:
                    root = root
                else:
                    root = root
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'oxo' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'oxo' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    if marker_type != 'causative':
                        root = 'o' + root
                    prefix = 'oxom'
                elif marker_type == 'causative':
                    prefix = 'oxo'
                else:
                    prefix = 'oxo'
                    
            # special handling for "ok̆o" 
            elif preverb == 'ok̆o':
                if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')):
                        preverb = preverb[:-1]
                if marker:
                    root = root
                else:
                    root = root
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    if marker_type != 'causative' and marker_type != 'applicative':
                        root = marker + root
                    first_letter = get_first_letter(root)
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = 'ok̆o' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    if marker_type != 'causative' and marker_type != 'applicative':
                        root = marker + root
                    first_letter = get_first_letter(root)
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'ok̆o' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    if marker_type != 'causative':
                        root = 'o' + root
                    prefix = 'ok̆om'
                elif marker_type in ('causative', 'applicative'):
                    prefix = preverb
                    print(f"Adjusted preverb: {preverb}, Subject marker: {subject_markers[subject]}, Root before adjustment: {root}")
                else:
                    prefix = preverb

            # Special handling for "go"

            else:
                # Adjust the prefix based on the first letter for phonetic rules
                if preverb:
                    preverb_form = preverbs_rules.get(preverb, preverb)
                    if isinstance(preverb_form, dict):
                        preverb_form = preverb_form.get(subject, preverb)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                            first_letter = get_first_letter(root)
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + 'm'
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix(preverb_form, first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + adjusted_prefix
                    else:
                        prefix = preverb_form
                else:
                    prefix = subject_markers[subject]
                    if obj in ['O2_Singular', 'O2_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                            first_letter = get_first_letter(root)
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = 'm' + prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix(prefix, first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = adjusted_prefix

            # Handle the Ardeşen rule
            if third_person.endswith('y'):
                if subject == 'S3_Singular':
                    root = root  # Ardeşen Exception root for S3 cases
                else:
                    root = root[:-1] + 'ms'  # Ardeşen Exception root for non-S3 cases - added an s to this in past tense to simplify code

            
            # Handle applicative marker and specific suffix replacement - if we have to remove the causative "o" for oxo/ok̆o preverbs, we could check here: if preverb ends with "o") root[:-1
            if applicative and causative:
                if root in ('oşums', 'oşups', 'odums'):
                    root = root[:-3] + 'vap'
                elif root.endswith(('ams', 'ups', 'oms', 'aps', 'ops', 'ums')):
                    root = root[:-3] + 'ap'
                elif root.endswith('umers') or root.endswith('amers'):
                    root = root[:-5] + 'ap'
                elif root.endswith('rs'):
                    root = root[:-1] + 'ap'
                elif root.endswith('y'):
                    root = root[:-2] + 'ap'
            elif applicative:
                if root in ('işums', 'işups', 'idums'):
                    root = root[:-3] + 'v'
                elif root.endswith(('ams', 'ups', 'oms', 'aps', 'ops', 'ums')):
                    root = root[:-3]
                elif root.endswith('y'):
                    root = root[:-2]
            elif causative:
                if root == 'digurams':
                    root = root
                elif root in ('oşums', 'oşups', 'odums'):
                    root = root[:-3] + 'vap'
                elif root.endswith(('ams', 'ups', 'oms', 'aps', 'ops', 'ums')):
                    root = root[:-3] + 'ap'
                elif root.endswith('umers') or root.endswith('amers'):
                    root = root[:-5] + 'ap'
                elif root.endswith('rs'):
                    root = root[:-1] + 'ap'
                elif root.endswith('y'):
                    root = root[:-2] + 'ap'
            else:
                if root in ('şums', 'şups', 'dums'):  # remove "am/um/ups" endings from root
                    root = root[:-3] + 'v'
                elif root.endswith(('ams', 'ups', 'oms', 'aps', 'ops', 'ums')):
                    root = root[:-3]
                elif root.endswith('y'):
                    root = root[:-2]
                elif root.endswith(('umers', 'amers')) and root == 'dumers':
                    root = root[:-5] + 'v'
                else:
                    root = root
                
            # Determine the suffix
            if subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular', 'O3_Plural']:
                suffix = 'asunon' if region == "HO" else 'asere' if region == "PZ" else 'asen'
            elif subject in ('S1_Singular') and obj in ('O1_Singular', 'O2_Singular', 'O3_Singular', 'O3_Plural'):
                suffix = 'aminon' if region == "HO" else 'are'
            elif subject in ('S2_Singular') and obj in ('O1_Singular', 'O2_Singular', 'O3_Singular', 'O3_Plural'):
                suffix = 'aginon' if region == "HO" else 'are'
            elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                suffix = 'sunonan' if region == "HO" else 'anere' if region == "PZ" else 'anen'
            elif subject in ('S1_Singular', 'S1_Plural') and obj in ['O2_Plural']:
                suffix = 'aminonan' if region == "HO" else 'atere' if region == "PZ" else 'aten'
            elif subject in ('S2_Singular', 'S2_Plural') and obj in ['O1_Plural']:
                suffix = 'aginonan' if region == "HO" else 'atere' if region == "PZ" else 'aten'
            elif subject == 'S3_Plural' and infinitive == 'oxenu' and region == 'HO':         # exception for future tense "oxenu" in Xopa 
                suffix = 'unonan'
            elif subject == 'S3_Plural':
                suffix = 'asunonan' if region == "HO" else 'atere' if region == "PZ" else 'anen'
            else:
                suffix = suffixes[subject]

            # Determine the final root to use
            final_root = root[:-1] if root.endswith('s') else root
            
            if infinitive == 'oxenu' and subject in ('S1_Singular', 'S1_Plural') and not applicative and not causative: # oxenu future tense exception
                prefix = 'p̌'
                final_root = ''
            elif infinitive == 'oxenu' and subject in ('S2_Singular', 'S2_Plural') and not applicative and not causative:
                prefix = 'q' if region == "HO" else ''
                final_root = '' if region in ('AŞ', 'PZ') else 'v'

            elif infinitive == 'oxenu' and subject in ('S3_Plural') and region == "HO" and not applicative and not causative:
                prefix = 'q'
                final_root = 'van'
            
            elif infinitive == 'oxenu' and subject in ('S3_Singular', 'S3_Plural') and not applicative and not causative:
                prefix = 'q' if region == "HO" else ''
                final_root = '' if region in ('AŞ', 'PZ') else 'va' if region == "HO" else 'v'

            # Conjugate the verb
            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    
    return region_conjugations


# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_future(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative)
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
        personal_pronouns = get_personal_pronouns(region)  # Added line
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
    'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
    'O1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
    'O3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe'
}

subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']

# Function to get the first word of a compound verb
def get_first_word(verb):
    return verb.split()[0] if len(verb.split()) > 1 else ''


# Example usage for Sx conjugations with a specific object and marker
infinitive = 'geç̌k̆u'
obj = 'O3_Singular'
marker = 'applicative'  # Change to 'causative' or 'applicative' if needed
object_pronoun = personal_pronouns_general[obj]

print(f"All subject conjugations of infinitive '{infinitive}' with object '{object_pronoun}' and {marker} marker:")
all_conjugations = collect_conjugations(infinitive, subjects, obj=obj, causative=(marker == 'causative'), applicative=(marker == 'applicative'))
print(format_conjugations(all_conjugations))







# In[6]:


# Example usage for Sx
infinitive = 'oç̌aru'
print(f"All subject conjugations of infinitive '{infinitive}':")
all_conjugations = collect_conjugations(infinitive, subjects)
print(format_conjugations(all_conjugations))


# In[25]:


# Example usage for SxOx conjugations
infinitive = 'oç̌aru'
obj = 'O2_Plural'
object_pronoun = personal_pronouns_general[obj]
print(f"All subject conjugations of infinitive '{infinitive}' with object '{object_pronoun}':")
all_conjugations = collect_conjugations(infinitive, subjects, obj=obj)
print(format_conjugations(all_conjugations))


# In[14]:


# Example usage for specific subject and object conjugation
infinitive = 'eç̌opu'
subject = 'S1_Singular'
obj = 'O2_Singular'

# Conjugate the verb in future tense
conjugation_result = conjugate_future(infinitive, subject=subject, obj=obj)

# Format and print the results
formatted_result = format_conjugations(conjugation_result)
print(formatted_result)


# Example usage for Sx conjugations with a specific object and marker
infinitive = 'geç̌k̆u'
obj = 'O3_Singular'
marker = 'both'  # Change to 'causative' or 'applicative' or 'both' if needed
object_pronoun = personal_pronouns_general[obj]

# Determine the flags for causative and applicative based on the marker value
is_causative = marker in ['causative', 'both']
is_applicative = marker in ['applicative', 'both']

print(f"All subject conjugations of infinitive '{infinitive}' with object '{object_pronoun}' and {marker} marker:")
all_conjugations = collect_conjugations(infinitive, subjects, obj=obj, causative=is_causative, applicative=is_applicative)
print(format_conjugations(all_conjugations))



# In[33]:


# Example usage for Sx conjugations with a specific object and marker
infinitive = 'ceçamu'
obj = 'O3_Plural'
marker = 'causative'  # Change to 'causative' or 'applicative' if needed
object_pronoun = personal_pronouns_general[obj]

print(f"All subject conjugations of infinitive '{infinitive}' with object '{object_pronoun}' and {marker} marker:")
all_conjugations = collect_conjugations(infinitive, subjects, obj=obj, causative=(marker == 'causative'), applicative=(marker == 'applicative'))
print(format_conjugations(all_conjugations))





# In[ ]:




