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

def get_phonetic_rules(region: str, is_tvm: bool = False) -> tuple:
    """Get phonetic rules for a given region and verb type."""
    if is_tvm:
        if region == 'FA':
            phonetic_rules_v = {
                'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                'b': ['a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                'm': ['n']
            }
        else:
            phonetic_rules_v = {
                'v': ['a', 'e', 'i', 'o', 'u'],
                'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
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

    else:
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

    return phonetic_rules_v, phonetic_rules_g
