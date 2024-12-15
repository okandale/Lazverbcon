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
ordered_objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']

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
def handle_marker(infinitive, root, marker, subject, obj):
    if infinitive == 'doguru':
        root = root[1:]  # Remove the first character 'd' from the root
    if infinitive in ('oç̌ǩomu', 'oşǩomu') and marker == 'o':
        root = 'çams'
        marker = ''
    if infinitive in ('oxenu') and marker in ('u', 'i', 'o'):  # marker case for oxenu
        root = 'xenams'
    if infinitive in ('oxvenu') and marker in ('u', 'i', 'o'):  # marker case for oxenu
        root = 'xvenams'
    if infinitive in ('oç̌ǩomu') and marker in ('i', 'u'):
        root = 'ç̌ǩomums'
    if infinitive in ('gemgaru', 'cebgaru'):
        if marker in ['i', 'o', 'u']:
            root = root[:1] + marker + root[3:] 
    if root.startswith('gyo'): #special case for geç̌ǩu
        if root[2] in ['i', 'o']:
            if marker in ['i']:
                root = root[:1] + marker + root[3:]  # Replace the second character 'i' or 'o' with 'i' or 'o'
            elif marker == 'o':
                root = root[:1] + marker + root[3:] if subject in ('S1_Singular', 'S1_Plural') or obj in ('O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural') else root[1:] 
            elif marker == 'u':
                root = marker + root[2:]  # Replace the second character 'i' or 'o' with 'u'
    if root.startswith('co'): #special case for ceç̌u
        if root[1] in ['i', 'o']:
            if marker in ['i']:
                root = root[:1] + marker + root[2:]  # Replace the second character 'i' or 'o' with 'i' or 'o'
            elif marker == 'o':
                root = root[:1] + marker + root[2:] if subject in ('S1_Singular', 'S1_Plural') or obj in ('O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural') else marker + root[2:] 
            elif marker == 'u':
                root = 'u' + root[2:]  # Replace the second character 'i' or 'o' with 'u'
    if root.startswith(('i', 'u', 'o')):
        if marker in ['i', 'o', 'u']:
            root = marker + root[1:]
              # Replace the first 'i' or 'o' with 'i' or 'o'
        elif marker == 'u': # may be redundant now
            root = 'u' + root[1:]  # Replace the first 'i' or 'o' with 'u'
    else:
        root = marker + root
    return root

