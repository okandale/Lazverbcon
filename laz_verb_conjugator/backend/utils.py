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

# Shared constants
subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']
