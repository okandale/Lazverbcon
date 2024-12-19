from utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    get_phonetic_rules,
    get_personal_pronouns,
    get_preverbs_rules,
    presentperf_subject_markers as subject_markers,
    subjects
)
from dataloader import load_tvm_tve_presentperf

verbs, regions = load_tvm_tve_presentperf()

preverbs_rules = get_preverbs_rules('tvm_tve_presentperf')

def get_suffixes(region):
    suffixes = {
        'S1_Singular': 'un' if region in ('FA') else 'apun',
        'S2_Singular': 'un' if region in ('FA') else 'apun', 
        'S3_Singular': 'un' if region in ('FA') else 'apun',
        'S1_Plural': 'unan' if region in ('FA') else 'apunan' if region in ('AŞ', 'HO') else 'apuran',
        'S2_Plural': 'unan' if region in ('FA') else 'apunan' if region in ('AŞ', 'HO') else 'apuran',
        'S3_Plural': 'unan' if region in ('FA') else 'apunan' if region in ('AŞ', 'HO') else 'apuran'
    }
    return suffixes

def conjugate_present_perfect_form(infinitive, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    
    if applicative or causative:
        raise ValueError("This tense cannot have an applicative, causative or optative. ")
    if obj:
        raise ValueError("This tense cannot have an object.")
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
            personal_pronouns = get_personal_pronouns(region, 'tvm_tve_presentperf')
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region, is_tvm=True)
            
            # Set root to infinitive
            root = infinitive
            first_word = get_first_word(root)
            root = process_compound_verb(root)

            suffixes = get_suffixes(region)

            # Extract the preverb from the infinitive if it exists
            preverb = ''
            preverb_exceptions = {'oǩoreʒxu', 'oǩoru', 'oxop̌u'}  # Ensure this set is defined appropriately, add additionally to 256

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
            first_letter = get_first_letter(root)

            # Adjust the prefix based on the first letter for phonetic rules
            if preverb.endswith(('a','e','i','o','u')) and subject in subject_markers and subject_markers[subject].startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a', 'e', 'i', 'o', 'u')) and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                if root.startswith('gyo'):  # Add 'y' only for 'geç̌ǩu'
                    preverb = preverb[:-1] + 'y'
                else:
                    preverb = preverb # changed for gonǯǩu

            if preverb == "me" and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                preverb = "n"
                prefix = preverb + subject_markers[subject]
            elif preverb == "ce" and subject in ['S3_Singular', 'S3_Plural']:
                prefix = "c" + subject_markers[subject]
            elif preverb in ('gama', 'gam'):
                root = 'ç'
                preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gamo'
                prefix = preverb + subject_markers[subject]
            elif preverb == 'go' and subject in ('S3_Singular', 'S3_Plural'):
                prefix = "gv" + subject_markers[subject] if region in ('HO') else "g" + subject_markers[subject]
            elif preverb == 'e' and subject in ('S3_Singular', 'S3_Plural'):
                prefix = "y" + subject_markers[subject]
            elif preverb:
                if preverb.endswith(('a', 'e', 'i', 'o', 'u')) and subject_markers[subject].startswith(('a', 'e', 'i', 'o', 'u')):
                    preverb = preverb[:-1]
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