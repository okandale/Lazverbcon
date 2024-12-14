def process_compound_verb(verb):
    """Process compound verbs and return the latter part."""
    return ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb

def get_first_letter(root):
    """Handle special letters in roots."""
    if len(root) > 1 and root[:2] in ['t̆', 'ç̌', 'ǩ', 'p̌', 'ǯ']:
        return root[:2]
    elif root.startswith('gyoç̌ǩams'):
        return root[2:]
    return root[0]

def get_first_word(verb):
    """Get the first word of a compound verb."""
    return verb.split()[0] if len(verb.split()) > 1 else ''

def remove_first_character(root):
    return root[1:]

def get_first_vowel_index(word):
    """Find the index of the first vowel in a word."""
    vowels = "aeiou"
    for index, char in enumerate(word):
        if char in vowels:
            return index
    return -1

def is_vowel(char):
    """Check if a character is a vowel."""
    return char in 'aeiou'



def adjust_prefix(prefix, first_letter, phonetic_rules):
    """Adjust prefix based on phonetic rules."""
    for p, letters in phonetic_rules.items():
        if first_letter in letters:
            return p
    return prefix

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

# Shared constants
subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']


"""
# from tvm_tve_presentperf and tvm_tve_passive and tvm_tense and ivd_pastpro and ivd_past and ivd_future
# Define personal pronouns outside of regions
personal_pronouns_general = {
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
    'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
    'O3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe'
}


# from tvm_tve_potential
# Define personal pronouns outside of regions
personal_pronouns_general = {
    'O1_Singular': 'ma',
    'O2_Singular': 'si',
    'O3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else '(h)emus',
    'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
    'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
    'O3_Plural': 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes'
}

# from all ivd modules and tve_present and tvm_tense and all tvm_tve modules

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

# for all tve modules except tve_present 

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

"""