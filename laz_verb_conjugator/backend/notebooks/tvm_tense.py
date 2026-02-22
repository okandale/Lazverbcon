from ..utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    is_vowel,
    adjust_prefix, 
    get_personal_pronouns,
    get_preverbs_rules,
    subjects
)

from backend.dataloader import load_tvm_tense

verbs, regions, co_verbs, gyo_verbs, no_verbs = load_tvm_tense()

preverbs_rules = get_preverbs_rules('tvm_tense')

# Phonetic rules for 'v' and 'g' ff
def get_phonetic_rules(region):
    if region == 'FA':
        phonetic_rules_v = {
            'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h', 'p'],
            'b': ['a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ',],
            'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
            'm': ['n']
        }
    else:
        phonetic_rules_v = {
            'v': ['a', 'e', 'i', 'o', 'u'],
            'p': ['p', 't', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
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
    return ''

# Function to handle marker and special case for verbs starting with 'i' or 'o'
def handle_marker(infinitive, root, marker):
    if infinitive == 'doguru':
        root = root[1:]  # Remove the first character 'd' from the root
    elif root.startswith('i') or root.startswith('o'):
        if marker in ['i', 'o']:
            root = marker + root[1:]  # Replace the first 'i' or 'o' with 'i' or 'o'
        elif marker == 'u':
            root = 'u' + root[1:]  # Replace the first 'i' or 'o' with 'u'
    else:
        root = marker + root
    return root

def get_suffixes(tense, region):
    suffixes = {}
    if tense == 'present':
        suffixes = {
            'S1_Singular': 'r',
            'S2_Singular': 'r',
            'S3_Singular': 'n',
            'S1_Plural': 'rt',
            'S2_Plural': 'rt',
            'S3_Plural': 'nan'
        }
    elif tense == 'future':
            suffixes = {
                'S1_Singular': 'aminon' if region == "HO" else 'are',
                'S2_Singular': 'aginon' if region == "HO" else 'are',
                'S3_Singular': 'sunon' if region == "HO" else 'asere' if region == "PZ" else 'asen',
                'S1_Plural': 'aminonan' if region == "HO" else 'asere' if region == "PZ" else 'aten',
                'S2_Plural': 'aginonan' if region == "HO" else 'atere' if region == "PZ" else 'aten',
                'S3_Plural': 'asunonan' if region == "HO" else 'anere' if region == "PZ" else 'anen'
        }
    elif tense == 'past':
        suffixes = {
            'S1_Singular': 'i',
            'S2_Singular': 'i',
            'S3_Singular': 'u',
            'S1_Plural': 'it',
            'S2_Plural': 'it',
            'S3_Plural': 'ey' if region == "AŞ" else 'es'
        }
    elif tense == 'past progressive':
        suffixes = {
            'S1_Singular': 'rt̆i',
            'S2_Singular': 'rt̆i',
            'S3_Singular': 'rt̆u',
            'S1_Plural': 'rt̆it',
            'S2_Plural': 'rt̆it',
            'S3_Plural': 'rt̆ey' if region == "AŞ" else 't̆es'
        }
    elif tense == 'optative':
        suffixes = {
            'S1_Singular': 'a',
            'S2_Singular': 'a',
            'S3_Singular': 'as',
            'S1_Plural': 'at',
            'S2_Plural': 'at',
            'S3_Plural': 'an'
        }
    return suffixes

def conjugate_verb(infinitive, tense, subject=None, obj=None, applicative=False, causative=False, simple_causative=False, use_optional_preverb=False):
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    

    if applicative and obj is None:
        raise ValueError("Applicative requires an object to be specified.")
    if (causative or simple_causative) and obj is None:
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
            personal_pronouns = get_personal_pronouns(region, 'tvm_tense')
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)

            suffixes = get_suffixes(tense, region)

            # Extract the preverb from the infinitive if it exists
            preverb = ''
            preverb_exceptions = {'gonǯǩu'}  # Ensure this set is defined appropriately, add additionally to 256

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
                
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)

            if root in ('imxors', 'ipxors') and infinitive == 'oç̌ǩomu':
                root = 'ç̌ǩomums'
            elif root in ('imxors') and infinitive == 'oşǩomu':
                root = 'şǩomums'
                
            # Remove the preverb from the third-person form if it exists
            if preverb and root.startswith(preverb) and infinitive != 'gonǯǩu':
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
            elif infinitive == 'oxoǯonu' and (subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural']):
                marker = 'o'  # Default to 'o' for oxoǯonu if neither applicative nor causative

            if infinitive == 'oxenu' and marker in ('u', 'i', 'o'):  # marker case for oxenu
                root = 'xenums'
            
            # Handle special case for verbs starting with 'i' or 'o'
            root = handle_marker(main_infinitive, root, marker)

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)

            # Special handling for "me"
            if preverb.endswith(('a','e','i','o','u')) and marker.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and marker.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and infinitive not in gyo_verbs and preverb != 'me':
                preverb = preverb[:-1]
            # Special handling for "me"
            print(F"preverb: {preverb}")
            prefix = ''
            if preverb == 'me' or (use_optional_preverb and not preverb):
                if root.startswith('no'):
                    if subject in ('S1_Singular', 'S1_Plural'):
                        root = root[2:]
                    else:
                        root = root[1:]
                        preverb = ''
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = preverb + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = 'mom'
                else:
                    prefix = 'me'
                
                if is_vowel(prefix[-1]) or is_vowel(root[-1]) and subject not in ('S1_Singular', 'S1_Plural'):
                    preverb = 'n'
                else:
                    preverb = 'me'

            if use_optional_preverb and not preverb:
                prefix = 'ko' + prefix
                if subject in ['O3_Singular', 'O3_Plural']:
                    prefix = 'k'
            # Special handling for "do"
            elif preverb == 'do':
                if root.startswith("di"): # Changed to 'di' from 'digurams', 'diguraps' to see if it's a general rule
                    root = root[1:]
                    prefix = 'do' + ('b' if region == 'FA' else 'v') if subject in ('S1_Singular', 'S1_Plural') else 'd'
                elif obj in ['O2_Singular', 'O2_Plural']:
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

            # Special handling for "geç̌ǩu"
            elif preverb == 'ge':
                if infinitive in gyo_verbs or root.startswith('gya'):
                    if subject in ['S1_Singular', 'S1_Plural']:
                        root = root[2:]
                    else:
                        root = root
                        preverb = ''
                else:
                    root = root
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = preverb + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = preverb + 'm'
                elif marker_type == 'causative':
                    prefix = ''
                else:
                    prefix = preverb if subject in ('S1_Singular', 'S1_Plural') or obj in ('O2_Singular', 'O2_Plural') else preverb[:1] if infinitive in gyo_verbs else preverb

           # Special handling for "ceç̌alu"
            elif preverb == 'ce':
                if infinitive in co_verbs:
                    if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                        root = root if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root[2:]  # Remove only one character if there's a marker
                    else:
                        root = root[1:]
                elif root.startswith('ca'):
                    if subject in ['S1_Singular', 'S1_Plural']:
                        root = root[1:]
                    else:
                        root = root
                        preverb = ''
                else:
                    if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                        root = root
                    else:
                        root = root
                first_letter = get_first_letter(root)
                if infinitive in ('ceyonu') and not marker: # add for other tenses
                    root = 'i' + root[2:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                first_letter = get_first_letter(root)
                if obj in ['O2_Singular', 'O2_Plural']:
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = preverb + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    prefix = preverb + 'm'
                elif marker_type == 'causative':
                    prefix = ''
                else:
                    prefix = preverb[:1] if root.startswith(('a','e','i','o','u')) else preverb

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
                    
            # special handling for "oǩo" 
            elif preverb == 'oǩo':
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
                    prefix = 'oǩo' + adjusted_prefix
                elif subject in ['S1_Singular', 'S1_Plural']:
                    if marker_type != 'causative' and marker_type != 'applicative':
                        root = marker + root
                    first_letter = get_first_letter(root)
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = 'oǩo' + adjusted_prefix
                elif obj in ['O1_Singular', 'O1_Plural']:
                    if marker_type != 'causative':
                        root = 'o' + root
                    prefix = 'oǩom'
                elif marker_type == 'causative':
                    prefix = 'oǩo'
                else:
                    prefix = 'oǩo'
            # Special handling for "go"
            else:
                # Adjust the prefix based on the first letter for phonetic rules
                print(F"root: {root}")
                if preverb:
                    if preverb == 'mo' and root.startswith('ma'):
                        if subject in ['S1_Singular', 'S1_Plural']:
                            root = root[1:]
                        else:
                            root = root
                            preverb = ''
                    elif preverb == 'gama':
                        if subject in ('S1_Singular', 'S1_Plural'):
                            preverb = 'gama'
                            root = root[3:]
                        else:
                            preverb = 'gam'
                            root = root[3:]
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        prefix = preverb + 'm'
                    elif marker_type == 'causative':
                        prefix = ''
                    else:
                        prefix = preverb
                else:
                    if obj in ['O2_Singular', 'O2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = adjusted_prefix
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

            # Handle applicative marker and specific suffix replacement - if we have to remove the causative "o" for oxo/oǩo preverbs, we could check here: if preverb ends with "o") root[:-1
            if marker_type == 'applicative' and root in ('işums', 'işups', 'idums'):
                root = root[:-3] + 'vap'
            elif marker_type == 'applicative' and (root.endswith('ums') or root.endswith('ams')):
                root = root[:-3] + 'ap'
            elif marker_type == 'causative' and root == 'digurams':
                root = root
            elif marker_type == 'causative' and root in ('oşums', 'oşups', 'odums'):
                root = root[:-3] + 'vap'
            elif marker_type == 'causative' and (root.endswith('ums') or root.endswith('ams')):
                root = root[:-3] + 'ap'
            elif marker_type == 'causative' and (root.endswith('umers') or root.endswith('amers')):
                root = root[:-5] + 'ap'
            elif marker_type == 'causative' and root.endswith('rs'):
                root = root[:-1] + 'ap'
            else:
                if root in ('şums', 'şups', 'dums'):  # remove "am/um/ups" endings from root
                    root = root[:-3] + 'v'
                elif root.endswith(('ums', 'ams', 'ups', 'aps')):
                    root = root[:-3]
                elif root.endswith('y'):
                    root = root[:-2]
                elif root.endswith(('umers', 'amers')) and root == 'dumers':
                    root = root[:-5] + 'v'
                else:
                    root = root
                
            # Determine the suffix
            if tense in ('future', 'past', 'optative'):
                root = root[:-2]
                suffix = suffixes[subject]
            else:
                root = root[:-1]
                suffix = suffixes[subject]

            # Determine the final root to use
            final_root = root[:-1] if root.endswith('s') else root
            
            if infinitive in ('oxtimu', 'olva') and subject in ('S1_Singular', 'S1_Plural') and tense in ('past', 'future', 'optative') and not applicative and not causative: # oxtimu tense exception
                final_root = 'id'
            elif infinitive in ('oxtimu', 'olva') and subject in ('S2_Singular', 'S2_Plural') and tense in ('past', 'future', 'optative') and not applicative and not causative:
                final_root = 'id'
            elif infinitive in ('oxtimu', 'olva') and subject in ('S3_Singular', 'S3_Plural') and tense in ('past', 'future', 'optative') and not applicative and not causative:
                final_root = 'id'
            elif infinitive == "ren" and subject in ('S1_Singular') and tense == 'present':
                if region in ("FA", "HO"):
                    prefix = "b" if region == "FA" else "v"
                final_root = 'ore'
                suffix = ''
            elif infinitive == "ren" and subject in ('S2_Singular') and tense == 'present':
                final_root = "(o)re"
                suffix = ''
            elif infinitive == "ren" and subject in ('S3_Singular') and tense == 'present':
                final_root = 'on' if region in ('PZ', 'AŞ') else "(o)ren"
                suffix = ''
            elif infinitive == "ren" and subject in ('S1_Plural') and tense == 'present':
                if region in ("FA", "HO"):
                    prefix = "b" if region == "FA" else "v"
                final_root = 'ore'
                suffix = 'rtu' if region == "AŞ" else 't'
            elif infinitive == "ren" and subject in ('S2_Plural') and tense == 'present':
                final_root = '(o)re'
                suffix = 'rtu' if region == "AŞ" else 't'
            elif infinitive == "ren" and subject in ('S3_Plural') and tense == 'present':
                final_root = 'on' if region in ('AŞ') else "(o)ren" if region in ('FA', 'HO') else "(o)" 
                suffix = 'ran' if region == "PZ" else 'an'
                    

            if infinitive == "ren" and tense in ('past', 'future'):
                if region in ("FA", "HO") and subject in ('S1_Singular', 'S1_Plural'):
                    prefix = "b" if region == "FA" else "v"
                final_root = 'ort̆'
                
            # Remove the first letter of final_root if it is the same as the last letter of prefix
            if prefix and final_root and prefix[-1] == final_root[0]:
                final_root = final_root[1:]    

            # Conjugate the verb
            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    return region_conjugations

def collect_conjugations_all(infinitive, subjects, tense='present', obj=None, applicative=False, causative=False, simple_causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_verb(infinitive, tense, subject=subject, obj=obj, applicative=applicative, causative=causative, simple_causative=simple_causative)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations

# Define the function to extract negative imperatives
def extract_neg_imperatives(all_conjugations, subjects):
    imperatives = {}
    for region, conjugations in all_conjugations.items():
        imperatives[region] = []
        for subject, obj, conjugation in conjugations:
            if subject in subjects:
                # Add "mot" to the conjugation
                conjugation_with_mot = f"mot {conjugation}"
                imperatives[region].append((subject, obj, conjugation_with_mot))
    return imperatives

# Function to format the negative imperative forms
def format_neg_imperatives(imperatives):
    result = {}
    for region, conjugations in imperatives.items():
        personal_pronouns = get_personal_pronouns(region, 'tvm_tense')
        formatted_conjugations = []
        
        # Sort conjugations to ensure S2_Singular appears before S2_Plural
        conjugations.sort(key=lambda x: 0 if x[0] == 'S2_Singular' else 1)
        
        for subject, obj, conjugation in conjugations:
            subject_pronoun = personal_pronouns[subject]
            obj_pronoun = personal_pronouns_general.get(obj, '')
            formatted_conjugations.append(f"{subject_pronoun} {obj_pronoun}: {conjugation}")
        result[region] = formatted_conjugations
    return result

def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, simple_causative=False, use_optional_preverb=False):
    return collect_conjugations_all_subjects_specific_object(infinitive, subjects, obj, applicative, causative, simple_causative, use_optional_preverb)