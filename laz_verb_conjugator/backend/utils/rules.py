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


def get_preverbs_rules(mode):
    if mode in ['ivd_future', 'ivd_past', 'ivd_pastpro']:
        return {
            ('ge', 'e', 'cel', 'ce', 'do', 'ye'): {
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
            ('ge', 'e', 'cel', 'ce', 'do', 'ye'): {
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
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye'): {
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
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye', 'cele'): {
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
            ('ge', 'e', 'cel', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'mo', 'ǩoǩo'): {
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
            ('ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye'): {
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
            ('ge', 'e', 'cele', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 'mo', 'ye'): {
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
