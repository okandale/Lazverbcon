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
    subjects,
    objects
)
from dataloader import load_tve_verbs

verbs, regions, co_verbs, gyo_verbs, no_verbs = load_tve_verbs()

preverbs_rules = get_preverbs_rules('tve_pastpro')

# Update the conjugate_past_progressive function to return a dictionary
def conjugate_past_progressive(infinitive, subject=None, obj=None, applicative=False, causative=False, use_optional_preverb=False):

    
    # Check for invalid SxOx combinations
    if applicative and (
        (subject == 'S1_Singular' and obj == 'O1_Plural') or 
        (subject == 'S2_Singular' and obj == 'O2_Plural') or
        (subject == 'S1_Plural' and obj == 'O1_Singular') or
        (subject == 'S2_Plural' and obj == 'O2_Singular')
    ):
        return {region: [(subject, obj, 'N/A - Geçersiz Kombinasyon')] for region in regions[infinitive]}
    elif (subject in ['S1_Singular', 'S1_Plural'] and obj in ['O1_Singular', 'O1_Plural'] and not applicative) or \
        (subject in ['S2_Singular', 'S2_Plural'] and obj in ['O2_Singular', 'O2_Plural'] and not applicative):
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
            personal_pronouns = get_personal_pronouns(region, 'tve_pastpro')
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            original_root = process_compound_verb(third_person)  # Store the original root before any modifications 
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)
            root = process_compound_verb(root)

            suffixes = {
                'S1_Singular': 't̆i',
                'S2_Singular': 't̆i',
                'S3_Singular': 't̆u',
                'S1_Plural': 't̆it',
                'S2_Plural': 't̆it',
                'S3_Plural': 't̆ey' if region == "AŞ" else 't̆es' # Ardeşen rule
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

            if infinitive in ('oxenu') and marker in ('u', 'i', 'o'):  # marker case for oxenu
                root = 'xenums'

            if infinitive in ('oxvenu') and marker in ('u', 'i', 'o'):  # marker case for oxenu
                root = 'xenums'            
            
            # Handle special case for verbs starting with 'i' or 'o'
            root = handle_marker(main_infinitive, root, marker, subject, obj)


            # Get the first letter after the marker is attached
            first_letter = get_first_letter(root)
            adjusted_prefix = ''

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

                if preverb == 'mo' or infinitive.startswith('mo'):
                    if root.startswith(('mu', 'imu', 'umu', 'omu')):
                        if root.startswith(('mu', 'imu', 'umu', 'omu')):
                            if not marker:
                                root = 'i' + root[2:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                            if marker:
                                root = marker + root[3:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[3:]
                        else:
                            if marker:
                                root = marker + root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[2:]                            
                            if not marker:
                                root = root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                            else:
                                root = marker + root[3:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[2:]
                        preverb = 'm' if subject in ('S2_Singular', 'S3_Singular', 'S2_Plural', 'S3_Plural') and obj in ('O3_Singular', 'O3_Plural') else 'm' if subject in ('S2_Singular', 'S2_Plural') and not obj else preverb
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        preverb = 'm' if adjusted_prefix.startswith(('a', 'e', 'i', 'o', 'u')) else preverb
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = 'mom'
                    else:
                        prefix = ''
                    if (infinitive.startswith('mo') and 
                        (not original_root.startswith(('mo', 'mu')) or 
                        (original_root.startswith('mu') and 
                        subject in ('S3_Singular', 'S3_Plural') and 
                        obj is None))):
                        preverb = preverb[:1]  # Remove the 'o' from preverb                  
                # Special handling for "me"
                if preverb == 'me' or (use_optional_preverb and not preverb):
                    if infinitive in no_verbs:
                        if root.startswith(('nu', 'inu', 'unu', 'onu')):
                            if not marker:
                                root = 'i' + root[2:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                            if marker:
                                root = marker + root[3:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[3:]
                        else:
                            if marker:
                                root = marker + root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[2:]                            
                            if not marker:
                                root = root[1:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                            else:
                                root = marker + root[3:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else marker + root[2:]
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        preverb = 'n' if root.startswith(('a', 'e', 'i', 'o', 'u')) else preverb
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = 'mem' if infinitive in no_verbs else 'mom'
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

                # Special handling for "ceç̌alu"
                elif preverb == 'gol':
                    if root.endswith('ams'):
                        if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] or obj in ['O3_Singular', 'O3_Plural'] and marker:
                            if applicative and causative:
                                root = root
                            if applicative:
                                root = root
                            elif causative:
                                root = root
                            else:
                                root = 'o' + root  # Remove only one character if there's a marker
                        else:
                            root = root
                            preverb = preverb
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + 'o' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + 'o' + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'o' + 'm'
                    elif marker_type == 'causative':
                        prefix = preverb 
                    else:
                        prefix = preverb

                # Special handling for "ceç̌alu"
                elif preverb == 'gelo':
                    if root.endswith('ams'):
                        if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] or obj in ['O3_Singular', 'O3_Plural'] and marker:
                            if applicative and causative:
                                root = root
                            if applicative:
                                root = root
                            elif causative:
                                root = root
                            else:
                                root = 'o' + root  # Remove only one character if there's a marker
                        else:
                            root = root
                            preverb = preverb
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'm'
                    elif marker_type == 'causative':
                        prefix = preverb 
                    else:
                        prefix = preverb

                # Special handling for "do"
                # Special handling for "do"
                elif preverb == 'do' or infinitive.startswith('do'):
                    if root.startswith(('du', 'idu', 'udu', 'odu')) and infinitive not in 'dodumu':  # Changed to 'di' from 'digurams', 'diguraps' to see if it's a general rule
                        root = root[1:] if root.startswith('du') else root[2:]
                        preverb = 'do' if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] else 'd'
                        if applicative:
                            if obj in ['O1_Singular', 'O1_Plural', 'O2_Singular', 'O2_Plural']:
                                root = marker + root
                        if causative:
                            root = marker + root[1:]
                        else:
                            root = 'i' + root[2:] if subject in ['S1_Singular', 'S1_Plural'] and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] else root
                    first_letter = get_first_letter(root)
                    if root.startswith('di'): # Changed to 'di' from 'digurams', 'diguraps' to see if it's a general rule
                        root = root[1:]
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        if root in ('iguraps', 'igurams'):
                            prefix = 'do' + 'b' if region == "FA" else 'do' + 'v'
                        else:
                            adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                            prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'm'
                    elif marker_type == 'causative' or main_infinitive == 'doguru':  # to prevent double 'o's in causative form and S1O3 conjugations for doguru
                        prefix = 'd'
                    else:
                        prefix = preverb

                # Special handling for "geç̌ǩu"
                elif preverb == 'ge' or infinitive.startswith('ge') or root.startswith(('igyu', 'ugyu', 'ogyu')):
  
                    if infinitive == 'gemgaru':
                        if marker:
                            root = marker + root[3:]
                        else:
                            if subject in ('S1_Singular', 'S1_Plural') or obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'):
                                root = root[2:]
                            else:
                                preverb = ''
                    if infinitive in gyo_verbs:
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:  
                            if root.startswith(('igyu', 'ugyu', 'ogyu')):
                                root = marker + root[4:]
                            else:
                                root = 'u' + root[2:] if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root[2:]  # Remove only one character if there's a marker                      
                        elif subject in ('S2_Singular', 'S2_Plural', 'S3_Singular', 'S3_Plural') and marker:
                            if root.startswith(('igyu', 'ugyu', 'ogyu')):
                                root = 'y' + marker + root[4:] if applicative or applicative and causative else 'gy' + marker + root[4:]
                            else:
                                root = 'yu' + root[2:] if applicative or applicative and causative else 'gy' + root[2:] 
                        else:
                            root = root[2:] if subject in ('S1_Singular', 'S1_Plural') or obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                    
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'm'
                    elif marker_type == 'causative':
                        prefix = ''
                    else:
                        prefix = preverb if subject in ('S1_Singular', 'S1_Plural') or obj in ('O2_Singular', 'O2_Plural') else preverb[:1] if infinitive in gyo_verbs else preverb

                # Special handling for "ceç̌alu"
                elif preverb == 'cel':
                    if infinitive in ('celabalu'):
                        if subject in ['S1_Singular', 'S1_Plural'] or obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']:
                            if applicative and causative:
                                root = 'i' + root[5:]
                            if applicative:
                                root = 'i' + root[5:]
                            elif causative:
                                root = 'o' + root[5:]
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
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + 'e' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + 'e' + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'em'
                    elif marker_type == 'causative':
                        prefix = preverb + 'a'
                    else:
                        prefix = preverb + 'a'


                # Special handling for "ceç̌alu"
                elif preverb == 'ce' or infinitive.startswith('ce'):
                    if infinitive in co_verbs or root.startswith(('icu', 'ocu', 'ucu')):
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in ['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural'] and marker:
                            if root.startswith(('icu', 'ucu', 'ocu')):
                                root = 'c' + marker + root[3:] if (applicative and causative or causative) and subject in (('S2_Singular', 'S3_Singular', 'S3_Plural')) and obj in ('O3_Singular', 'O3_Plural') else marker + root[3:]
                            else:
                                root = root if subject in ('S1_Singular', 'S1_Plural') and marker == 'u' else root[2:]  # Remove only one character if there's a marker
                        else:
                            if marker and subject in 'S3_Singular' and obj in 'O2_Plural':
                                root = marker + root[3:]
                            else:
                                if marker:
                                    root = 'c' + marker + root[3:] if (applicative and causative or causative) and subject in (('S2_Singular', 'S3_Singular', 'S2_Plural', 'S3_Plural')) and obj in ('O3_Singular', 'O3_Plural') and root.startswith(('icu', 'ucu', 'ocu')) else root[2:]
                                else:
                                    root = 'c' + 'o' + root[3:] if subject in (('S2_Singular', 'S3_Singular', 'S2_Plural', 'S3_Plural')) and obj in ('O3_Singular', 'O3_Plural') else root[1:]
                                    preverb = '' if subject in (('S2_Singular', 'S3_Singular', 'S2_Plural', 'S3_Plural')) and obj in ('O3_Singular', 'O3_Plural') else 'ce'
                    else:
                        if marker and obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural']: #remove this redundant part if not necessary
                            root = root
                        else:
                            root = root
                    first_letter = get_first_letter(root)

                    if root.startswith(('ca', 'ic', 'uc', 'oc')):
                        if infinitive == 'cebgaru' and marker:
                            root = root[:3] + 'b' + root[3:]
                        if subject in ['S1_Singular', 'S1_Plural'] and marker or obj in [['O2_Singular', 'O3_Singular', 'O3_Plural' 'O2_Plural', 'O1_Singular', 'O1_Plural']] and marker:
                            if marker:
                                root = root[2:]
                            else:
                                root = root[1:]  # Remove only one character if there's a marker
                        elif subject in ['S1_Singular', 'S1_Plural'] or subject in ['S3_Singular', 'S3_Plural'] and obj in ['O2_Singular', 'O2_Plural']:
                            root = root[2:] if obj in ['O2_Plural', 'O2_Singular'] and marker else root[1:]  # no idea why but marker and S3 x O2_plural combination lead to this line
                            preverb = 'ce'
                        elif obj in ['O1_Singular', 'O1_Plural', 'O2_Plural']:
                            root = root[2:] if marker else root[1:]
                            preverb = 'ce'
                        else:
                            root = root
                            preverb = ''
                    if infinitive in ('ceyonu') and not marker: # add for other tenses
                        root = 'i' + root[2:] if obj in ('O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural') else root[1:]
                    first_letter = get_first_letter(root)
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                        prefix = preverb + 'm'
                    elif marker_type == 'causative':
                        prefix = ''
                    else:
                        prefix = preverb[:1] if root.startswith(('a','e','i','o','u')) else preverb
                    if root.startswith(('ic', 'uc', 'oc')):
                        root = root[1:]
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
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        first_letter = get_first_letter(root)
                        root = root[1:] if marker and subject == 'S3_Singular' and obj == 'O2_Plural' else root
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = preverb + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
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
                    if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                        first_letter = get_first_letter(root)
                        root = root[1:] if marker and subject == 'S3_Singular' and obj == 'O2_Plural' else root
                        adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        prefix = 'oǩo' + adjusted_prefix
                    elif subject in ['S1_Singular', 'S1_Plural']:
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        if root.startswith('n'):
                            root = root[1:]
                        prefix = preverb + adjusted_prefix
                    elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
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
                    if preverb or infinitive.startswith('gama'):    # add more preverbs here perhaps
                        preverb_form = preverbs_rules.get(preverb, preverb)
                        if isinstance(preverb_form, dict):
                            preverb_form = preverb_form.get(subject, preverb)
                        elif (preverb in 'gama' or infinitive.startswith(('gama', 'igama')) and not root.startswith('gama') and 
                            (subject in ['S1_Singular', 'S1_Plural'] or 
                            obj in ['O2_Singular', 'O2_Plural', 'O1_Singular', 'O1_Plural'])):
                            root = root[1:] if original_root.startswith('gamaça') else root
                            if marker:
                                root = marker + root[1:]                          
                            preverb = 'gama'
                            preverb_form = 'gama'
                        if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                            if root.startswith('n'):
                                root = root[1:]  # Remove the initial 'n'
                                first_letter = get_first_letter(root)
                                adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                                prefix = preverb + 'n' + adjusted_prefix  # Add 'n' back before the adjusted prefix
                            else:
                                first_letter = get_first_letter(root)
                                adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                                prefix = preverb + adjusted_prefix
                        elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
                            if root.startswith('n'):
                                root = root[1:]
                            prefix = preverb + 'm'
                        elif subject in ['S1_Singular', 'S1_Plural']:
                            first_letter = get_first_letter(root)
                            adjusted_prefix = adjust_prefix(preverb_form, first_letter, phonetic_rules_v)
                            if root.startswith('n'):
                                root = root[1:]
                            prefix = preverb + adjusted_prefix
                        else:
                            prefix = preverb_form
                    else:
                        prefix = subject_markers[subject]
                        
                        if root == 'oroms':
                            if obj in ('O2_Singular', 'O2_Plural') and not subject in ['S2_Singular', 'S2_Plural']:
                                prefix = 'ǩ'
                            elif subject in ('S1_Singular', 'S1_Plural') and obj in ('O3_Singular', 'O3_Plural'):
                                prefix = 'p̌'
                            elif subject in ('S1_Singular', 'S1_Plural'):
                                prefix = 'p̌'
                            elif obj in ('O1_Singular', 'O1_Plural') and not subject in ['S1_Singular', 'S1_Plural']:
                                prefix = 'p̌'
                            else:
                                prefix = subject_markers[subject]
                        if obj in ['O2_Singular', 'O2_Plural'] and not subject in ['S2_Singular', 'S2_Plural']:
                            prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                        elif obj in ['O1_Singular', 'O1_Plural'] and not subject in ['S1_Singular', 'S1_Plural']:
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
                    root = root[:-1] + 'ms'  # Ardeşen Exception root for non-S3 cases - added an s to this in past tense to simplify code


            
            # Handle applicative marker and specific suffix replacement - if we have to remove the causative "o" for oxo/oǩo preverbs, we could check here: if preverb ends with "o") root[:-1
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
                elif root.endswith('rs'):
                    root = root[:-1] + ('aps' if region == "HO" else 'ams')                
            elif causative:
                if root == ('çams'): #changed root for oç̌ǩomu/oşǩomu
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
                
            # Determine the suffix
            if subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular', 'O3_Plural']:
                suffix = 't̆u'
            elif subject in ('S1_Singular', 'S2_Singular') and obj in ('S1_Singular', 'S2_Singular', 'S3_Singular', 'S3_Plural'):
                suffix = 't̆i'
            elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                suffix = 't̆es'
            elif subject in ['S1_Plural', 'S2_Plural']:
                suffix = 't̆it'
            elif subject == 'S3_Plural':
                suffix = 't̆ey' if region == "AŞ" else 't̆es'
            else:
                suffix = suffixes[subject]



            # Determine the final root to use
            final_root = root[:-1] if root.endswith('s') else root

            # Remove the first letter of final_root if it is the same as the last letter of prefix
            if prefix and final_root and prefix[-1] == final_root[0]:
                final_root = final_root[1:]

            # Conjugate the verb
            conjugated_verb = f"{prefix}{final_root}{suffix}"
            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_past_progressive(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations

def collect_conjugations_all_subjects_all_objects(infinitive, applicative=False, causative=False, use_optional_preverb=False):
    all_conjugations = {}
    for subject in subjects:
        for obj in objects:
            result = conjugate_past_progressive(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
            for region, conjugation_list in result.items():
                if region not in all_conjugations:
                    all_conjugations[region] = set()
                for conjugation in conjugation_list:
                    all_conjugations[region].add((subject, obj, conjugation[2]))
    return all_conjugations

def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, use_optional_preverb=False):
    return collect_conjugations(infinitive, subjects, obj, applicative, causative, use_optional_preverb)