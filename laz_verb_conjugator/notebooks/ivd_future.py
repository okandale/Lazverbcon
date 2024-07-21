import pandas as pd

# Load the spreadsheet
file_path = r'C:\Users\Adam\Documents\Okan\Laz\Machine Learning\Dictionary\Test Verb Present tense.xlsx'

# Read the Excel file
df = pd.read_excel(file_path, engine='openpyxl')

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

# Function to process compound verbs and return the latter part
def process_compound_verb(verb):
    return ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb

# Define preverbs and their specific rules
preverbs_rules = {
    ('ge', 'e', 'ce', 'd'): {
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

# Function to handle special letters
def get_first_letter(root):
    if len(root) > 1 and root[:2] in ['t̆', 'ç̌', 'k̆', 'p̌']:
        return root[:2]
    return root[0]

# Function to handle special letters
def get_first_vowel_index(word):
    vowels = "aeiou"
    for index, char in enumerate(word):
        if char in vowels:
            return index
    return -1

# Function to handle the specific case for verbs starting with 'u' and verbs with 'i' in the root
def handle_special_case_u(root, subject, preverb):
    if root.startswith('u'):
        if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
            root = 'i' + root[1:]

    if preverb == 'd':
        first_vowel_index = get_first_vowel_index(root)
        if first_vowel_index != -1 and root[first_vowel_index] == 'i':
            if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                root = root[:first_vowel_index] + 'a' + root[first_vowel_index + 1:]
        else:
            root = root

    return root

# Function to handle special case for 'gy' preverb
def handle_special_case_gy(root, subject):
    if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
        root = root[0] + root[1:]
    return root

# Function to handle special case for 'coz' preverb
def handle_special_case_coz(root, subject):
    return 'ozun'

# Function to remove the first character for certain roots
def remove_first_character(root):
    return root[1:]

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else 'hiyas',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hiya',
        'S1_Plural': 'çku' if region == "FA" else 'şk̆u' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region in ('FA', 'HO') else 't̆k̆va' if region in ('AŞ', 'PZ') else 'tkva',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# Function to conjugate future tense with subject and object, handling preverbs, phonetic rules, applicative and causative markers
def conjugate_future(infinitive, subject, obj=None, applicative=False, causative=False, use_optional_preverb=False):
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
            
            # Process the compound root to get the main part
            root = process_compound_verb(third_person)
            first_word = get_first_word(third_person)  # Get the first word for compound verbs
            root = process_compound_verb(root)

            subject_markers = {
                'S1_Singular': 'm',
                'S2_Singular': 'g',
                'S3_Singular': '',
                'S1_Plural': 'm',
                'S2_Plural': 'g',
                'S3_Plural': ''
            }
        
            suffixes = {
                'S1_Singular': 'rt̆asen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'asen',
                'S2_Singular': 'rt̆asen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'asen',
                'S3_Singular': 'rt̆asen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'asen',
                'S1_Plural': 'rt̆anen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'anen',
                'S2_Plural': 'rt̆anen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'anen',
                'S3_Plural': 'rt̆anen' if infinitive in ('oçkinu', 'uğun', 'uyonun', 'unon') else 'anen',
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

            # Remove second character 'v' if it exists and the subject is not S3
            if preverb in ('go', 'd') and len(root) > 1 and root[1] == 'v' and subject in ['S1_Singular', 'S1_Plural', 'S2_Singular', 'S2_Plural']:
                root = root[0] + root[2:]


            # Remove first character of the root if the preverb is 'go'
            if preverb == 'go' and len(root) > 0:
                root = remove_first_character(root)

            if preverb == 'd' and len(root) > 0 and root[0] == 'v' and subject in ['S1_Singular', 'S2_Plural', 'S1_Plural', 'S2_Singular']:
                root = remove_first_character(root)

            # Determine the final root to use
            final_root = root[:-2]

            # Adjust the prefix based on the preverb and subject
            if preverb:
                preverb_form = preverbs_rules.get((preverb,), {}).get(subject, preverb)
                prefix = preverb_form
            else:
                prefix = subject_markers[subject]

            # Determine the suffix
            suffix = suffixes[subject]
            if obj:
                if subject == 'S3_Singular' and obj in ['O1_Singular', 'O3_Singular', 'O2_Singular']:
                    suffix = 'u'
                elif subject == 'S3_Singular' and obj in ['O1_Plural', 'O2_Plural']:
                    suffix = 'es'
                elif subject in ['S1_Singular', 'S2_Singular'] and obj in ['O1_Singular', 'O2_Singular']:
                    suffix = 'i'
                elif subject in ['S1_Singular', 'S2_Singular'] and obj in ['O3_Singular', 'O3_Plural']:
                    suffix = 'u'
                elif subject in ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural'] and obj == 'S3_Singular':
                    suffix = 'es'
                elif subject in ['S3_Plural'] and obj == 'S3_Plural':
                    suffix = 'es'
                elif subject in ['S1_Singular', 'S1_Plural'] and obj == 'O2_Plural':
                    suffix = 'it'
                elif subject in ['S2_Singular', 'S2_Plural'] and obj == 'S1_Plural':
                    suffix = 'itt'

            # Specific rule for S1O2 and S2O1 conjugations: replace ending 'n' with 'r'
            if suffix == 'r' and root.endswith('n'):
                final_root = root[:-1]

            # Specific case: preverb minus last character and root minus first character for certain preverbs
            if preverb in ('ge', 'e', 'ce', 'd'):
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'om'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'og'
                elif subject in ['S3_Singular', 'S3_Plural']:
                    prefix = preverb

            elif preverb in ('go'):
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb + 'm'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb + 'g'
                elif subject in ['S3_Singular', 'S3_Plural']:
                    prefix = preverb[:-1]

            elif preverb in ('gy'):
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = preverb[:1] + 'em'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = preverb[:1] + 'eg'
                elif subject in ['S3_Singular', 'S3_Plural']:
                    prefix = preverb[:1] + 'y'
                    
            elif preverb in ('coz'):
                if subject in ['S1_Singular', 'S1_Plural']:
                    prefix = 'cem'
                elif subject in ['S2_Singular', 'S2_Plural']:
                    prefix = 'ceg'
                elif subject in ['S3_Singular', 'S3_Plural']:
                    prefix = 'c'

            if use_optional_preverb and not preverb:
                prefix = 'ko' + prefix
                if subject in ['O3_Singular', 'O3_Plural']:
                    prefix = 'k'

            # Conjugate the verb
            if preverb in ('go', 'gy', 'coz'):
                if suffix == 'r' and root.endswith('n'):
                    final_root = root[:-1]
                    conjugated_verb = f"{prefix}{final_root}{suffix}"
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root[:-1]
                    conjugated_verb = f"{prefix}{final_root}{suffix}"
                else:
                    conjugated_verb = f"{prefix}{final_root}{suffix}"
            elif preverb == 'd':
                if suffix == 'r' and root.endswith('n'):
                    final_root = root[:-1]
                    conjugated_verb = f"{prefix}{final_root}{suffix}"
                elif root.endswith('s'):
                    final_root = root[:-1]
                    conjugated_verb = f"{prefix}{final_root}{suffix}"
                else:
                    conjugated_verb = f"{prefix}{root}{suffix}"
            else:
                if suffix == 'r' and root.endswith('n'):
                    final_root = root[:-1]
                elif subject in ['S1_Plural', 'S2_Plural', 'S3_Plural'] and root.endswith('s'):
                    final_root = root[:-2]
                elif root.endswith('en'):
                    final_root = root[:-2
                                      
                                      ]
                else:
                    final_root = root[:-1]
                conjugated_verb = f"{prefix}{final_root}{suffix}"

            region_conjugations[region].append((subject, obj, f"{first_word} {conjugated_verb}".strip()))

    return region_conjugations

# Define the function to handle conjugations and collection
def collect_conjugations(infinitive, subjects, obj=None, applicative=False, causative=False, use_optional_preverb=False):
    all_conjugations = {}
    for subject in subjects:
        result = conjugate_future(infinitive, subject=subject, obj=obj, applicative=applicative, causative=causative, use_optional_preverb=use_optional_preverb)
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
    'O3_Singular': 'heya',
    'O3_Plural': 'hentepe',
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O1_Plural': 'çku',
    'O2_Plural': 'tkva'
}

subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']

# Function to get the first word of a compound verb
def get_first_word(verb):
    return verb.split()[0] if len(verb.split()) > 1 else ''