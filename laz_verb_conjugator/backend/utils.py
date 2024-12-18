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
ordered_objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']

def get_phonetic_rules(region: str, is_tvm: bool = False) -> tuple:
    """Get phonetic rules for a given region and verb type."""
    if is_tvm:
        if region == 'FA':
            phonetic_rules_v = {
                'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                'b': ['a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                'm': ['b', 'n']
            }
        else:
            phonetic_rules_v = {
                'v': ['a', 'e', 'i', 'o', 'u'],
                'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                'b': ['b', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
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
                'm': ['b', 'n']
            }
        else:
            phonetic_rules_v = {
                'v': ['a', 'e', 'i', 'o', 'u'],
                'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                'b': ['b', 'l', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
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
    if infinitive in ('oşǩomu') and marker in ('i', 'u'):
        root = 'şǩomums'
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
# ivd
ivd_subject_markers = {
                'S1_Singular': 'm',
                'S2_Singular': 'g',
                'S3_Singular': '',
                'S1_Plural': 'm',
                'S2_Plural': 'g',
                'S3_Plural': ''
            }

# tve, tvm_tense, tvmtve passive
tve_subject_markers = {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }

# tvm tve presentperf
presentperf_subject_markers = {
                'S1_Singular': 'mi',
                'S2_Singular': 'gi',
                'S3_Singular': 'u',
                'S1_Plural': 'mi',
                'S2_Plural': 'gi',
                'S3_Plural': 'u'
            }

# tvm tve potential
potential_subject_markers = {
                'S1_Singular': 'ma',
                'S2_Singular': 'ga',
                'S3_Singular': 'a',
                'S1_Plural': 'ma',
                'S2_Plural': 'ga',
                'S3_Plural': 'a'
            }

def get_preverbs_rules(mode):
    if mode in ['ivd_future', 'ivd_past', 'ivd_pastpro']:
        return {
            ('ge', 'e', 'cel', 'ce', 'do', 'ye', 'me', 'mola', 'mo', 'oǩo', 'ǩoǩo'): {
                'S1_Singular': 'm',
                'S2_Singular': 'g',
                'S3_Singular': '',
                'S1_Plural': 'm',
                'S2_Plural': 'g',
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
    elif mode in ['ivd_present']:
        return {
            ('ge', 'e', 'cel', 'ce', 'do', 'ye', 'me', 'mola', 'mo', 'oǩo', 'ǩoǩo'): {
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
    elif mode in ['tve_past', 'tve_pastpro']:
        return {
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mola', 'ye', 'mo', 'ǩoǩo'): {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }
        }
    elif mode in ['tve_future']:
        return {
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye', 'cele', 'mola', 'mo', 'ǩoǩo'): {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }
        }
    elif mode in ['tve_present']:
        return {
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mola', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'mo', 'ǩoǩo'): {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }
        }
    elif mode in ['tvm_tense']:
        return {
            ('ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye', 'mola', 'mo', 'ǩoǩo'): {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }
        }
    elif mode in ['tvm_tve_passive', 'tvm_tve_potential', 'tvm_tve_presentperf']:
        return {
            ('ge', 'e', 'cele', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mola', 'mo', 'ye', 'ǩoǩo'): {
                'S1_Singular': 'v',
                'S2_Singular': '',
                'S3_Singular': '',
                'S1_Plural': 'v',
                'S2_Plural': '',
                'S3_Plural': ''
            }
        }

def get_personal_pronouns(region, mode):
    # Base pronouns that are always the same
    pronouns = {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
    }
    
    # Handle first/second person plurals with mode variations
    if mode == 'tvm_tve_passive':
        pronouns.update({
            'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
            'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
            'O1_Plural': 'çku',  # Always çku for O1_Plural in this mode
            'O2_Plural': 'tkva'  # Always tkva for O2_Plural in this mode
        })
    elif mode in ['ivd_present', 'ivd_future', 'ivd_past', 'ivd_pastpro', 'tvm_tense', 'tvm_tve_potential', 'tvm_tve_presentperf']:
        pronouns.update({
            'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else ('çkin' if mode == 'tvm_tve_potential' else 'çki'),
            'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
            'O1_Plural': 'çku',
            'O2_Plural': 'tkva'
        })
    else:  # tve modes
        if mode == 'tve_pastpro':
            pronouns.update({
                'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
                'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
                'O1_Plural': 'çku',
                'O2_Plural': 'tkva'
            })
        else:
            pronouns.update({
                'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
                'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
                'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
                'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan'
            })

    # Logic for S3_Singular
    if mode in ['ivd_present', 'ivd_future', 'ivd_past']:
        pronouns['S3_Singular'] = 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emus'
    elif mode == 'ivd_pastpro':
        pronouns['S3_Singular'] = 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else 'hemus'
    elif mode in ['tvm_tve_potential', 'tvm_tve_presentperf']:
        pronouns['S3_Singular'] = 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else '(h)emus'
    elif mode in ['tve_future', 'tve_past', 'tve_present', 'tve_pastpro']:
        pronouns['S3_Singular'] = 'heyak' if region == "FA" else 'himuk' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emuk'
    elif mode in ['tvm_tense', 'tvm_tve_passive']:
        pronouns['S3_Singular'] = 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em'

    # Logic for O3_Singular
    if mode in ['tve_present', 'tve_past', 'tve_future', 'tve_pastpro']:
        pronouns['O3_Singular'] = 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emus'
    elif mode == 'ivd_pastpro':
        pronouns['O3_Singular'] = 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hem'
    else:
        pronouns['O3_Singular'] = 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em'

    # Logic for S3_Plural
    if mode in ['tve_present', 'tve_future', 'tve_past']:
        pronouns['S3_Plural'] = 'hentepek' if region == "FA" else 'hinik' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepek'
    elif mode == 'tve_pastpro':
        pronouns['S3_Plural'] = 'hentepek' if region == "FA" else 'hinik' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepe'
    elif mode in ['ivd_present', 'ivd_future', 'ivd_past', 'ivd_pastpro']:
        pronouns['S3_Plural'] = 'hentepes' if region == "FA" else ('hini' if region == 'AŞ' else 'hinis' if region == 'PZ' else 'entepes')
    elif mode == 'tvm_tve_potential':
        pronouns['S3_Plural'] = 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes'
    elif mode == 'tvm_tve_presentperf':
        pronouns['S3_Plural'] = 'hentepes' if region == "FA" else ('hini' if region == 'AŞ' else 'hinis' if region == 'PZ' else 'entepes')
    else:
        pronouns['S3_Plural'] = 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe'

    # Logic for O3_Plural
    if mode in ['tve_present', 'tve_past', 'tve_future']:
        pronouns['O3_Plural'] = 'hentepes' if region == "FA" else 'hinis' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepes'
    elif mode == 'tve_pastpro':
        pronouns['O3_Plural'] = 'hentepes'
    else:
        pronouns['O3_Plural'] = 'hentepe'

    return pronouns