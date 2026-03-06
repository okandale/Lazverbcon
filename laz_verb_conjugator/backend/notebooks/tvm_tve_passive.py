# passive form with present, past, future, past progressive tense
# update similarily to potential form if all forms stay the same.
import pandas as pd
import os
from ..utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    is_vowel,
    adjust_prefix,
    get_phonetic_rules,
    get_personal_pronouns,
    get_preverbs_rules,
    tve_subject_markers as subject_markers,
    subjects
)
from backend.dataloader import load_tvm_tve_passive

verbs, regions = load_tvm_tve_passive()

preverbs_rules = get_preverbs_rules('tvm_tve_passive')

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

def conjugate_passive_form(infinitive, tense, subject=None, obj=None, applicative=False, causative=False, simple_causative=False, use_optional_preverb=False):
    
    # Check for invalid SxOx combinations
    if (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural']) or \
       (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural']):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    
    if applicative and (causative or simple_causative):
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
            personal_pronouns = get_personal_pronouns(region, 'tvm_tve_passive')
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region, is_tvm=True)
            
            # Set root to infinitive
            root = infinitive
            first_word = get_first_word(root)
            root = process_compound_verb(root)

            suffixes = get_suffixes(tense, region, causative)

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
                root = 'i' + root[len(preverb):-1]  # Remove only the preverb
            elif root in (('oşu', 'dodumu', 'otku')):
                root = 'i' + infinitive[1:-1] + "v"
            else:
                root = 'i' + root[1:-1]  # Remove the last character of the root

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)

            # Adjust the prefix based on the first letter for phonetic rules
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb != 'go' and preverb != 'me':
                preverb = preverb[:-1]
            
            
            prefix = subject_markers[subject]
            
            # Special handling for "me"
            if preverb == 'me' or (use_optional_preverb and not preverb):
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
                    prefix = 'n'
                
                if is_vowel(prefix[-1]) or is_vowel(root[-1]) and subject not in ('S1_Singular', 'S1_Plural'):
                    preverb = 'n'
                else:
                    preverb = 'me'
                    
            elif infinitive in ('gamaçamu'):
                root = 'iç'
                preverb = 'gam' if subject in ('S3_Singular', 'S3_Plural') else 'gamo'
                prefix = preverb + subject_markers[subject]
            elif (infinitive.startswith('gama') and not root.startswith('gama') and 
                (subject in ['S1_Singular', 'S1_Plural'] or 
                obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'])):
                preverb = 'gama'
                prefix = preverb + subject_markers[subject]            
            elif preverb == 'go' and root.startswith(('a','e','i','o','u')) and subject not in ('S1_Singular', 'S1_Plural'):
                prefix = "gv" + subject_markers[subject] if region in ('PZ', 'AŞ') else "gu" + subject_markers[subject] if region in 'HO' else "g" + subject_markers[subject]
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
def collect_conjugations_all(infinitive, subjects, tense='present', obj=None, applicative=False, causative=False, simple_causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_passive_form(infinitive, tense, subject=subject, causative=causative, simple_causative=simple_causative)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations
