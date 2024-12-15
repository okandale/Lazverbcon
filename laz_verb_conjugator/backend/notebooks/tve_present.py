# Most up-to-date formula with preverbs (ge [along with geç̌ǩu's exception), e, ce, dolo, do [along with 'doguru'], go, oxo (based on oxoǯonu) me (as actual preverb i.e. 'meçamu' not additional), applicative and object conjugation (and Ardeşen rule), now including causative marke. 
# directives ("me", "mo", "n") for non-preverb verbs are missing (i.e. oç̌aru - megiç̌aram)
# added "n" root changer - gomǯam (gonǯalu)
# added optional preverb 'me' and 'ko' - won't show up in conjugator
# added preverb 'gama'
# added regions and regional variences'
# added negative imperative
import pandas as pd
import os
from utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    adjust_prefix,
    is_vowel,
    get_phonetic_rules,
    determine_marker,
    handle_marker,
    get_personal_pronouns,
    get_preverbs_rules,
    tve_subject_markers as subject_markers,
    ordered_objects
)
from dataloader import load_tve_verbs

verbs, regions, co_verbs, gyo_verbs = load_tve_verbs()

preverbs_rules = get_preverbs_rules('tve_present')

# Function to conjugate present tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
def conjugate_present(infinitive, subject, obj=None, applicative=False, causative=False, use_optional_preverb=False, mood=None):
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
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)
        
            suffixes = {
                'S1_Singular': '',
                'S2_Singular': '',
                'S3_Singular': 's',
                'S1_Plural': 't',
                'S2_Plural': 't',
                'S3_Plural': 'an'
            }

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

                
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
                
            # Remove the preverb from the third-person form if it exists
            if preverb and root.startswith(preverb):
                root = root[len(preverb):]
            # After extracting third_person, root, and region but before preverb logic:


            # Determine the marker (applicative or causative)
            marker = ''
            marker_type = ''
            if applicative:
                marker = determine_marker(subject, obj, 'applicative')
                marker_type = 'applicative'
            elif causative:
                marker = determine_marker(subject, obj, 'causative')
                marker_type = 'causative'



            # Handle special case for verbs starting with 'i' or 'o'
            if marker:
                root = handle_marker(main_infinitive, root, marker, subject, obj)

            if mood == 'optative' and infinitive == 'oç̌ǩomu':
                    root = 'ç̌ǩomum'
            elif mood == 'optative' and infinitive == 'oşǩomu':
                    root = 'şǩomum'

            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)
            adjusted_prefix = ''


# Create a flag to track if we've handled gonǯǩu special case
            handled_gontzku = False

            if infinitive == 'gonǯǩu' and (obj in ('O3_Singular', 'O3_Plural') or obj is None) and not marker:
                preverb = ''  # Clear the preverb for special case
                if subject in ('S1_Singular', 'S1_Plural'):
                    prefix = 'bgo'
                else:
                    prefix = 'go'
                handled_gontzku = True  # Set the flag

            if not handled_gontzku:

                if preverb.endswith(('a','e','i','o','u')) and marker.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and preverb == 'e':
                    preverb = 'ey' if region == 'PZ' else 'y'
                if preverb.endswith(('a','e','i','o','u')) and marker.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and not obj in ('O1_Singular', 'O1_Plural', 'O2_Plural', 'O2_Singular') and infinitive not in gyo_verbs and preverb != 'me':
                    preverb = preverb[:-1] + 'y' if preverb == 'ge' else preverb[:-1] # added for 'geçamu' as it would omit the 'y' in (no S1) O3 conjugations. 
                # Special handling for "me"
                if preverb == 'me' or (use_optional_preverb and not preverb):
                    if infinitive in no_verbs:
                        if root.startswith('nu'):
                            root = 'ii' + root[2:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root
                        else:
                            root = 'i' + root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else 'u' + root[2:]                            
                        if not marker:
                            root = root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                        else:
                            root = marker + root[3:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[2:]
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        preverb = 'n' if root.startswith(('a', 'e', 'i', 'o', 'u')) else preverb
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        prefix = 'mom'
                    else:
                        prefix = 'me'
                    
                    if is_vowel(root[0]) and prefix.endswith(('a', 'i', 'u', 'o', 'e')) and not adjusted_prefix:
                        preverb = 'n'
                    else:
                        if prefix == 'mom':
                            preverb = 'mo'
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
                    if obj in ['O2_Singular', 'O2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = 'do' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        if root in ('iguraps', 'igurams'):
                            prefix = 'do' + 'b' if region == "FA" else 'do' + 'v'
                        else:
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
                    if infinitive in gyo_verbs:
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                            root = 'u' + root[2:] if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root[2:]  # Remove only one character if there's a marker
                        elif subject in ('S2_Singular', 'S2_Plural', 'S3_Singular', 'S3_Plural') and marker:
                            root = 'yu' + root[2:] if applicative or applicative and causative else 'gy' + root[2:] 
                        else:
                            root = root[2:] if subject in ('S1_Singular', 'S1_Plural') or obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
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
                elif preverb == 'ela':
                    if infinitive in ('elaşinu'):
                        if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] or obj in ['O3_Singular', 'O3_Plural'] and marker:
                            if applicative and causative:
                                root = 'i' + root[2:]
                            if applicative:
                                root = marker + root[2:] if obj in ('O3_Singular', 'O3_Plural') else marker + root[2:]
                            elif causative:
                                root = 'o' + root[2:]
                            else:
                                root = root[2:]  # Remove only one character if there's a marker
                        else:
                            root = root[1:]
                            preverb = preverb
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root[2:]
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
                        prefix = preverb 
                    else:
                        prefix = preverb[:2]


                # Special handling for "ceç̌alu"
                elif preverb == 'cel':
                    if infinitive in ('celabalu'):
                        if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] or obj in ['O3_Singular', 'O3_Plural'] and marker:
                            if applicative and causative:
                                root = 'i' + root[2:]
                            if applicative:
                                root = 'i' + root[2:]
                            elif causative:
                                root = 'o' + root[2:]
                            else:
                                root = 'o' + root[1:]  # Remove only one character if there's a marker
                        else:
                            root = root[1:]
                            preverb = preverb
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + 'e' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + 'e' + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        prefix = preverb + 'em'
                    elif marker_type == 'causative':
                        prefix = preverb 
                    else:
                        prefix = preverb + 'a'


                # Special handling for "ceç̌alu"
                elif preverb == 'ce':
                    if infinitive in co_verbs:
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                            root = root if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root[2:]  # Remove only one character if there's a marker
                        else:
                            root = root[1:]
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
                    if infinitive in ('oxoǯonu', 'oxoşkvinu'):
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                            root = root if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root  # Remove only one character if there's a marker
                        else:
                            root = 'o' + root
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        first_letter = get_first_letter(root)
                        root = root[1:] if marker and subject == 'S3_Singular' and obj == 'O2_Plural' else root
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + 'm'
                    elif marker_type in ('causative', 'applicative'):
                        prefix = preverb
                    else:
                        prefix = preverb


                # special handling for "oǩo" 
                elif preverb == 'oǩo':
                    if infinitive in ('oǩobğu'):
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                            root = root if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root  # Remove only one character if there's a marker
                        else:
                            root = 'o' + root
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural']:
                        first_letter = get_first_letter(root)
                        root = root[1:] if marker and subject == 'S3_Singular' and obj == 'O2_Plural' else root
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = 'oǩo' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural']:
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + 'm'
                    elif marker_type in ('causative', 'applicative'):
                        prefix = preverb
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
                                root = root[1:]  # Remove the initial 'n'
                                first_letter = get_first_letter(root)
                                adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                                prefix = preverb + 'n' + adjusted_prefix  # Add 'n' back before the adjusted prefix
                            else:
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



                        if root == 'oroms':
                            if obj in ('O2_Singular', 'O2_Plural'):
                                prefix = 'ǩ'
                            elif subject in ('S1_Singular', 'S1_Plural') and obj in ('O3_Singular', 'O3_Plural'):
                                prefix = 'p̌'
                            elif subject in ('S1_Singular', 'S1_Plural'):
                                prefix = 'p̌'
                            elif obj in ('O1_Singular', 'O1_Plural'):
                                prefix = 'p̌'
                            else:
                                prefix = subject_markers[subject]

                        else: 
                            if obj in ['O2_Singular', 'O2_Plural']:
                                if root.startswith('n'):
                                    root = root[1:]
                                    first_letter = get_first_letter(root)
                                prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                            elif obj in ['O1_Singular', 'O1_Plural']:
                                if root.startswith('n'):
                                    root = root[1:]
                                prefix = 'm' + prefix
                            elif subject in ['S1_Singular', 'S1_Plural']:
                                adjusted_prefix = adjust_prefix(prefix, first_letter, phonetic_rules_v)
                                if root.startswith('n'):
                                    root = root[1:]
                                prefix = adjusted_prefix
                            else:
                                prefix = subject_markers[subject]

            # Handle the Ardeşen rule
            if third_person.endswith('y'):
                if subject == 'S3_Singular':
                    root = root  # Ardeşen Exception root for S3 cases
                else:
                    root = root[:-1] + 'm'  # Ardeşen Exception root for non-S3 cases

            # Handle applicative marker and specific suffix replacement - if we have to remove the causative "o" for oxo/oǩo preverbs, we could check here: if preverb ends with "o") root[:-1 
            if applicative and causative:
                if infinitive in (('oşu', 'dodvu', 'otku')):
                    root = root[:-3] + ('vapap' if region == "HO" else 'vapam')  
                elif root.endswith(('umers', 'omers')) or root.endswith('amers'):
                    root = root[:-5] + 'apam'
                elif root.endswith(('ms', 'ps')): 
                    root = root[:-3] + ('apap' if region == "HO" else 'apam')
                elif root.endswith('ams'):
                    root = root[:-3] + 'apam'
                elif root.endswith('rs'):
                    root = root[:-1] + 'apam'
                elif root.endswith(('um', 'om', 'op')) or root.endswith('am'):
                    root = root[:-2] + ('apap' if region == "HO" else 'apam')
                elif root.endswith('y'):
                    root = root[:-2] + 'apam'
            elif applicative:
                if infinitive in (('oşu', 'dodvu', 'otku')):
                    root = root[:-3] + ('vaps' if region == "HO" else 'vams') 
                elif root.endswith(('ms', 'ups')):
                    root = root[:-3] + ('aps' if region == "HO" else 'ams')
                elif root.endswith(('um')):
                    root = root[:-2] + 'ams'
                elif root.endswith('y'):
                    root = root[:-2] + 'ams'
            elif causative:
                if root == ('çams'): #changed root for oç̌ǩomu/oşǩomu
                    root = root
                elif infinitive == 'doguru':
                    root = root
                elif infinitive in (('oşu', 'dodvu', 'otku')):
                    root = root[:-3] + ('vapap' if region == "HO" else 'vapam')  
                elif root.endswith('umers') or root.endswith('amers'):
                    root = root[:-5] + 'apam'
                elif root.endswith(('ms', 'ps')): 
                    root = root[:-3] + ('apap' if region == "HO" else 'apam')
                elif root.endswith('ams'):
                    root = root[:-3] + 'apam'
                elif root.endswith('rs'):
                    root = root[:-1] + ('apap' if region == "HO" else 'apam')
                elif root.endswith('um') or root.endswith('am'):
                    root = root[:-2] + 'apam'
                elif root.endswith('y'):
                    root = root[:-2] + 'apam'
            # Mood adjustment for root - add to the above markers if a combination of marker and mood is possible:

            if mood == 'optative' and infinitive in (('oşu', 'dodvu', 'otku')):
                if applicative and causative:
                    root = root[:-2]
                elif applicative:
                    root = root[:-3] + 'v'
                elif causative:
                    root = root[:-2]
                else:
                    root = root[:-3] + 'v' 
            elif mood == 'optative' and root.endswith(('ms', 'ps')):
                root = root[:-3]
            elif mood == 'optative' and root.endswith(('umers', 'amers')):
                root = root[:-5]
            elif mood == 'optative' and root.endswith('ums'):
                root = root[:-3]
            elif mood == 'optative' and root.endswith('ams'):
                root = root[:-3]
            elif mood == 'optative' and root.endswith(('um', 'am')):
                root = root[:-2]
            elif mood == 'optative' and root.endswith('y'):
                root = root[:-2]
            elif mood == 'optative' and root.endswith('rs'):
                root = root[:-1]
            elif mood == 'optative':
                root = root[:-2]


            # Determine the suffix
            if subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular'] and root.endswith('ms') and mood == 'optative':
                suffix = 'ay' if region == "AŞ" else 'as'
            elif subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular'] and root.endswith('ms'):
                if region == "AŞ":
                    if root.endswith('ms'):
                        root = root[:-2]
                    else:
                        root = root[:-1]
                    suffix = 'y' 
                else:
                    suffix = 's'
            elif subject == 'S3_Singular' and obj in ['O2_Plural', 'O1_Plural'] and root.endswith('ms') and region == "AŞ":
                suffix = 'man'
            elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O3_Plural', 'O2_Plural'] and root.endswith('ms'):
                    root = root[:-1]
                    suffix = 'an'
            elif subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular'] and root.endswith('y') and mood == 'optative':
                suffix = 'ay'
            elif subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular'] and root.endswith('y'):
                suffix = ''
            elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                suffix = 'man' if (root.endswith('m') and region == "AŞ") else 'an'
            elif subject in ('S1_Singular', 'S2_Singular') and mood == 'optative':
                suffix = 'a'
            elif subject in ('S1_Plural', 'S2_Plural') and mood == 'optative':
                suffix = 'at' if region == "AŞ" else 'at'
            elif subject in ['S1_Singular', 'S1_Plural'] and obj == 'O2_Plural':
                suffix = 't'
            elif subject in ['S2_Singular', 'S2_Plural'] and obj == 'O1_Plural':
                suffix = 't'
            elif subject == 'S3_Singular' and mood == 'optative':
                suffix = 'ay' if region == "AŞ" else 'as'
            elif subject == 'S3_Singular' and root.endswith(('um', 'am', 'ms')):
                if region == "AŞ":
                    if root.endswith('ms'):
                        root = root[:-2]
                    else:
                        root = root[:-1]
                    suffix = 'y'
                else:
                    suffix = 's'
            else:
                suffix = suffixes[subject]

            # Determine the final root to use
            if region == "AŞ" and root.endswith('apam') and subject == 'S3_Singular':
                final_root = root[:-1]
            elif region == "AŞ" and root.endswith('ms') and subject == 'S3_Singular':
                final_root = root[:-2]
            elif root.endswith('s'):
                final_root = root[:-1]
            else:
                final_root = root

            # Remove the first letter of final_root if it is the same as the last letter of prefix
            if prefix and final_root and prefix[-1] == final_root[0]:
                final_root = final_root[1:]


            # Conjugate the verb
            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))


    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, mood=None):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, mood=mood)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = []
            for conjugation in conjugation_list:
                all_conjugations[region].append((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    # Convert sets to lists for JSON serialization
    for region in all_conjugations:
        all_conjugations[region] = list(all_conjugations[region])
    return all_conjugations

def extract_neg_imperatives(all_conjugations, subjects):
    imperatives = {}
    for region, conjugations in all_conjugations.items():
        imperatives[region] = []
        for subject, obj, conjugation in conjugations:
            if subject in subjects:
                # Use "mo" for region "HO", otherwise "mot"
                neg_prefix = "mo" if region in ("HO", "AŞ") else "mot"
                conjugation_with_neg = f"{neg_prefix} {conjugation}"
                imperatives[region].append((subject, obj, conjugation_with_neg))
    return imperatives

def format_neg_imperatives(imperatives):
    result = {}
    for region, conjugations in imperatives.items():
        # Get both subject and object pronouns for this region
        subject_pronouns = get_personal_pronouns(region, 'tve_present')
        object_pronouns = get_personal_pronouns_general(region)
        
        formatted_conjugations = []
        for subject, obj, conjugation in conjugations:
            subject_pronoun = subject_pronouns[subject]
            obj_pronoun = object_pronouns.get(obj, '')
            formatted_conjugations.append(f"{subject_pronoun} {obj_pronoun}: {conjugation}")

        # Reorder for negative imperatives, ensuring S2_Singular comes before S2_Plural
        formatted_conjugations.sort(key=lambda x: (
            x.split()[0] == subject_pronouns['S2_Plural'],  # Place S2_Plural last
            x.split()[0] == subject_pronouns['S2_Singular'],  # Place S2_Singular first
            ordered_objects.index(x.split()[1]) if len(x.split()) > 1 and x.split()[1] in ordered_objects else -1
        ))
        
        result[region] = formatted_conjugations
    
    return result

def collect_conjugations_all_subjects_all_objects(infinitive, applicative=False, causative=False, use_optional_preverb=False, mood=None):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']
    all_conjugations = {}
    for subject in subjects:
        for obj in objects:
            result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb, mood=mood)
            for region, conjugation_list in result.items():
                if region not in all_conjugations:
                    all_conjugations[region] = []
                for conjugation in conjugation_list:
                    all_conjugations[region].append((subject, obj, conjugation[2]))
    # Convert sets to lists for JSON serialization
    for region in all_conjugations:
        all_conjugations[region] = list(all_conjugations[region])
    return all_conjugations



def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, use_optional_preverb=False, mood=None):
    subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    return collect_conjugations(infinitive, subjects, obj, applicative, causative, use_optional_preverb, mood)




# Define personal pronouns outside of regions
def get_personal_pronouns_general(region):
    return {
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O3_Singular': 'heyas' if region == "FA" else 'himus' if region == "PZ" else 'him' if region == "AŞ" else '(h)emus',
    'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
    'O3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == "PZ" else 'hini' if region == "AŞ" else 'entepes'
}

