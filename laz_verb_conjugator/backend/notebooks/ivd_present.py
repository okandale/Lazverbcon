from utils import (
    process_compound_verb,
    get_first_letter,
    get_first_word,
    handle_special_case_coz,
    handle_special_case_gy,
    handle_special_case_u,
    get_personal_pronouns,
    get_preverbs_rules,
    get_phonetic_rules,
    adjust_prefix,
    ivd_subject_markers as subject_markers,
    subjects,
    objects
)
from dataloader import load_ivd_verbs

verbs, regions = load_ivd_verbs()

preverbs_rules = get_preverbs_rules('ivd_present')

# Function to conjugate present tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
def conjugate_present(infinitive, subject, obj=None, applicative=False, causative=False, use_optional_preverb=False, mood=False):
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
            personal_pronouns = get_personal_pronouns(region, 'ivd_present')
            phonetic_rules_v, phonetic_rules_g = get_phonetic_rules(region)
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)

            if mood and obj:
                raise ValueError("Dative verbs cannot take an object in the optative.")
            # Use the first word from the infinitive consistently
            first_word = first_word_infinitive
        
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
            prefix = ''
            preverb_exceptions = {'oǩomandu'}
            if main_infinitive not in preverb_exceptions:
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
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and not subject in ('S1_Singular', 'S1_Plural') and preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            if preverb.endswith(('a','e','i','o','u')) and root.startswith(('a','e','i','o','u')) and preverb not in 'me':
                preverb = preverb[:-1] 

            # Special handling for "me"
            if preverb == 'me' or (use_optional_preverb and not preverb):
                if root.startswith('na') and subject not in ('S3_Singular', 'S3_Plural'):
                    root = root[1:]
                    prefix = preverb_form + 'm' if subject in ('S1_Singular', 'S1_Plural') else preverb + 'g'
                else:
                    if subject in ('S3_Singular', 'S3_Plural'):
                        if obj in ('O1_Singular', 'O1_Plural'):
                            adjusted_prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                            prefix = preverb + adjusted_prefix
                            root = root[1:]



            
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
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
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

            elif preverb == 'mo' or infinitive.startswith("mo"):
                if root.startswith('m') and subject not in (('S3_Singular', 'S3_Plural')):
                    root = root[1:]
                if subject in ('S3_Singular', 'S3_Plural') and obj in ('O1_Singular', 'O1_Plural'):
                    adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                    prefix = preverb + adjusted_prefix
                elif subject in ('S2_Singular', 'S2_Plural'):
                    adjusted_prefix = adjust_prefix('g', first_letter, phonetic_rules_g)
                    prefix = preverb + adjusted_prefix
                elif subject in ('S1_Singular', 'S1_Plural') and obj in ('O3_Singular', 'O3_Plural'):
                    adjusted_prefix = 'm'
                    prefix = preverb + adjusted_prefix
                else:
                    prefix = preverb[2:] + subject_markers[subject] if root.startswith('m') else preverb + subject_markers[subject]


            elif preverb:
                print(F"root: {root}")
                if root.startswith(('ca', 'adgi')):
                    if subject in ('S3_Singular', 'S3_Plural'):
                        preverb = 'c'
                    root = root if infinitive == 'cedginu' else root[1:]  # exception for ceginu present tense, 3rd person in particular (swallows 'c' if not used)
                    if subject in ('S1_Singular', 'S2_Singular', 'S1_Pural', 'S2_Plural'):
                        root = root[1:]
                if root.startswith(('ma', 'mu')):
                    root = root if subject in ('S3_Singular', 'S3_Plural') else root[1:]
                    preverb = '' if subject in ('S3_Singular', 'S3_Plural') else preverb
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'm'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'g'

                elif subject in ('S3_Singular', 'S3_Plural'):
                    if obj in ('O1_Singular', 'O1_Plural'):
                        adjusted_prefix = adjust_prefix('v', first_letter, phonetic_rules_v)
                        prefix = preverb + adjusted_prefix                    
                else:
                    prefix = preverb
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

            if mood == 'optative':
                root = root[:-2]
                suffix = 'az' if region in 'FA' and subject in (('S1_Singular', 'S2_Singular', 'S3_Singular')) else 'as' if subject in (('S1_Singular', 'S2_Singular', 'S3_Singular')) else 'an'
            else:
                if subject == 'S3_Singular' and (obj == 'O3_Singular' or obj is None):
                    suffix = ''
                elif subject == 'S3_Singular' and obj == 'O3_Plural':
                    if root.endswith(('rs', 'ns')):
                        root = root
                    suffix = ''
                elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                    if root.endswith(('en', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                    if root.endswith('ns'):
                        root = root[:-1]
                    suffix = 't'
                elif subject in ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S3_Plural'] and obj in ['O1_Singular', 'O2_Singular']:
                    if root.endswith(('n', 'rs')):
                        root = root[:-1]
                        suffix = '' if infinitive.endswith('rs') else 'r'
                    if root.endswith('ns'):
                        root = root[:-1]
                        suffix = ''
                elif subject in ['S1_Singular', 'S1_Plural', 'S2_Singular', 'S2_Plural', 'S3_Plural'] and obj in ('O1_Plural', 'O2_Plural'):
                    if root.endswith(('n', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                    if root.endswith('ns'):
                        root = root[:-1]
                    suffix = 't'
                elif subject in ['S1_Plural', 'S2_Plural'] and obj in ('O1_Singular', 'O2_Singular'):
                    if root.endswith(('n', 'rs')):
                        root = root[:-2] if infinitive.endswith('rs') else root[:-1]
                    suffix = 'rt'
                    if root.endswith('ns'):
                        root = root[:-1]
                    suffix = 't'
                elif subject in ['S1_Singular', 'S2_Singular'] and obj in ['O3_Singular', 'O3_Plural']:
                    suffix = ''
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Singular'] and (obj in ('O3_Singular', 'O3_Plural') or obj is None):
                    if root.endswith('rs') or root.endswith('ns'):
                        root = root[:-1]
                    suffix = '' if root.endswith('an') else 's' if infinitive == 'coxons' and subject == 'S3_Singular' else 'an'
                elif subject == 'S3_Plural':
                    if root.endswith('rs') or root.endswith('ns'):
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
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, use_optional_preverb=False, mood=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb, mood=mood)
        for region, conjugation_list in result.items():
            if region not in all_conjugations:
                all_conjugations[region] = set()
            for conjugation in conjugation_list:
                all_conjugations[region].add((subject, obj, conjugation[2]))  # Ensure unique conjugation for each combination
    return all_conjugations

def collect_conjugations_all_subjects_all_objects(infinitive, applicative=False, causative=False, use_optional_preverb=False, mood=False):
    all_conjugations = {}
    for subject in subjects:
        for obj in objects:
            result = conjugate_present(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb, mood=mood)
            for region, conjugation_list in result.items():
                if region not in all_conjugations:
                    all_conjugations[region] = set()
                for conjugation in conjugation_list:
                    all_conjugations[region].add((subject, obj, conjugation[2]))
    return all_conjugations

def collect_conjugations_all_subjects_specific_object(infinitive, obj, applicative=False, causative=False, use_optional_preverb=False, mood=None):
    return collect_conjugations(infinitive, subjects, obj, applicative, causative, use_optional_preverb, mood)




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

def extract_imperatives(all_conjugations, subjects):
    """
    all_conjugations: dict[region -> set((subject, obj, conjugation), ...)]
    subjects: e.g. ['S2_Singular', 'S2_Plural']
    """
    imperatives = {}
    for region, forms in all_conjugations.items():
        imperatives[region] = [
            (subj, obj, conj)
            for (subj, obj, conj) in forms
            if subj in subjects
        ]
    return imperatives


def process_imperative(self, infinitive, subject, obj, applicative, causative, region_filter):
    module = None
    mood = None

    if 'tve_past' in self.tense_modules and infinitive in self.tense_modules['tve_past'].verbs:
        module = self.tense_modules['tve_past']
        mood = None  # TVE imperative is from past (your existing logic)
    elif 'ivd_present' in self.tense_modules and infinitive in self.tense_modules['ivd_present'].verbs:
        module = self.tense_modules['ivd_present']
        mood = 'optative'  # <-- KEY for IVD imperative

    if not module:
        return None

    subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
    objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]

    all_conjugations = {}
    for subj in subjects:
        for obj_item in objects:
            result = self._call_conjugation_method(
                module, infinitive, [subj], obj_item,
                applicative=applicative, causative=causative, mood=mood
            )
            for region, forms in result.items():
                if region_filter and region not in region_filter.split(','):
                    continue
                all_conjugations.setdefault(region, set()).update(forms)

    imperatives = module.extract_imperatives(all_conjugations, subjects)
    return self.format_conjugations(imperatives, module)


# Define personal pronouns outside of regions for IVD
def get_personal_pronouns_general(region):
    """General personal pronouns for object reference in IVD"""
    return {
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O3_Singular': 'heyas' if region == "FA" else 'himus' if region == "PZ" else 'him' if region == "AŞ" else '(h)emus',
        'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'O3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == "PZ" else 'hini' if region == "AŞ" else 'entepes'
    }