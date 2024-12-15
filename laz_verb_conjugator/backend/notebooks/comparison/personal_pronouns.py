# ivd present, future, past
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# ivd past pro
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else 'hemus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else 'hem',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# tve future, past
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyak' if region == "FA" else 'himuk' if region == "PZ" else 'him' if region == "AŞ" else '(h)emuk',
        'O3_Singular': 'heyas' if region == "FA" else 'himus' if region == "PZ" else 'him' if region == "AŞ" else '(h)emus',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepek' if region == "FA" else 'hinik' if region == "PZ" else 'hini' if region == "AŞ" else 'entepek',
        'O3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == "PZ" else 'hini' if region == "AŞ" else 'entepes',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan'
    }

#tve pastpro
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyak' if region == "FA" else 'himuk' if region == "PZ" else 'him' if region == "AŞ" else '(h)emuk',
        'O3_Singular': 'heyas' if region == "FA" else 'himus' if region == "PZ" else 'him' if region == "AŞ" else '(h)emus',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepek' if region == "FA" else 'hinik' if region == "PZ" else 'hini' if region == "AŞ" else 'entepe',
        'O3_Plural': 'hentepes',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# tve present
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyak' if region == "FA" else 'himuk' if region == "PZ" else 'him' if region == "AŞ" else '(h)emuk',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepek' if region == "FA" else 'hinik' if region == "PZ" else 'hini' if region == "AŞ" else 'entepek',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O3_Singular': 'heyas' if region == "FA" else 'himus' if region == "PZ" else 'him' if region == "AŞ" else '(h)emus',
        'O1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'O2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'O3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == "PZ" else 'hini' if region == "AŞ" else 'entepes'
    }

# tvm tense
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# tvm tve passive

def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepe' if region == "FA" else 'hini' if region in ('AŞ', 'PZ') else 'entepe',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# tvm tve potential
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else '(h)emus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çkin',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region in ('AŞ', 'PZ') else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }

# tvm tve presentperf
def get_personal_pronouns(region):
    return {
        'S1_Singular': 'ma',
        'S2_Singular': 'si',
        'S3_Singular': 'heyas' if region == "FA" else 'himus' if region in ('AŞ', 'PZ') else '(h)emus',
        'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
        'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
        'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
        'S3_Plural': 'hentepes' if region == "FA" else 'hini' if region in ('AŞ') else 'hinis' if region == 'PZ' else 'entepes',
        'O3_Plural': 'hentepe',
        'O1_Singular': 'ma',
        'O2_Singular': 'si',
        'O1_Plural': 'çku',
        'O2_Plural': 'tkva'
    }