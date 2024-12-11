export function getPersonalPronouns(region) {
    return {
      'S1_Singular': 'ma',
      'S2_Singular': 'si',
      'S3_Singular': region === "FA" ? 'heyas' : 
                     region === 'PZ' ? 'himus' : 
                     region === 'AŞ' ? 'him' : '(h)emus',
      'O3_Singular': region === "FA" ? 'heya' : 
                     region === 'AŞ' || region === 'PZ' ? 'him' : '(h)em',
      'S1_Plural': region === "FA" ? 'çku' : 
                   region === 'AŞ' || region === 'PZ' ? 'şǩu' : 'çki',
      'S2_Plural': region === "FA" ? 'tkva' : 
                   region === 'AŞ' || region === 'PZ' ? 't̆ǩva' : 'tkvan',
      'S3_Plural': region === "FA" ? 'hentepes' : 
                   region === 'PZ' ? 'hinis' : 
                   region === 'AŞ' ? 'hini' : 'entepes',
      'O3_Plural': 'hentepe',
      'O1_Singular': 'ma',
      'O2_Singular': 'si',
      'O1_Plural': 'çku',
      'O2_Plural': 'tkva'
    };
  }