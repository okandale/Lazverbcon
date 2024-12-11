export const PreverbRules = {
    groups: {
      basic: ['ge', 'e', 'ce', 'dolo', 'do', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'ǩoǩo'],
      go: ['go'],
      gy: ['gy'],
      coz: ['coz'],
      me: ['me'],
      oxo: ['oxo'],
      oǩo: ['oǩo'],
      gama: ['gama']
    },
  
    modifiers: {
      basic: {
        'S1_Singular': 'om',
        'S2_Singular': 'og',
        'S3_Singular': '',
        'S1_Plural': 'om',
        'S2_Plural': 'og',
        'S3_Plural': ''
      },
      go: {
        'S1_Singular': 'gom',
        'S2_Singular': 'gog',
        'S3_Singular': 'go',
        'S1_Plural': 'gom',
        'S2_Plural': 'gog',
        'S3_Plural': 'go'
      },
      gy: {
        'S1_Singular': 'gem',
        'S2_Singular': 'geg',
        'S3_Singular': 'gyo',
        'S1_Plural': 'gem',
        'S2_Plural': 'geg',
        'S3_Plural': 'gyo'
      },
      coz: {
        'S1_Singular': 'cem',
        'S2_Singular': 'ceg',
        'S3_Singular': 'coz',
        'S1_Plural': 'cem',
        'S2_Plural': 'ceg',
        'S3_Plural': 'coz'
      },
      oxo: {
        'S1_Singular': 'oxov',
        'S2_Singular': 'oxog',
        'S3_Singular': 'oxo',
        'S1_Plural': 'oxov',
        'S2_Plural': 'oxog',
        'S3_Plural': 'oxo'
      },
      oǩo: {
        'S1_Singular': 'oǩov',
        'S2_Singular': 'oǩog',
        'S3_Singular': 'oǩo',
        'S1_Plural': 'oǩov',
        'S2_Plural': 'oǩog',
        'S3_Plural': 'oǩo'
      },
      gama: {
        'S1_Singular': 'gamav',
        'S2_Singular': 'gamag',
        'S3_Singular': 'gama',
        'S1_Plural': 'gamav',
        'S2_Plural': 'gamag',
        'S3_Plural': 'gama'
      }
    },
  
    past: {
      base: {
        'S1_Singular': 'u',
        'S2_Singular': 'u',
        'S3_Singular': 'u',
        'S1_Plural': 'es',
        'S2_Plural': 'es',
        'S3_Plural': 'es'
      },
      withObject: {
        'S3_Singular': {
          'O3_Singular': 'u',
          'O3_Plural': 'es',
          'O1_Plural': 'es',
          'O2_Plural': 'es'
        },
        'S1_Singular': {
          'O1_Singular': 'i',
          'O2_Singular': 'i',
          'O3_Singular': 'u',
          'O3_Plural': 'es'
        }
      }
    },
  
    future: {
      base: {
        'S1_Singular': 'asen',
        'S2_Singular': 'asen',
        'S3_Singular': 'asen',
        'S1_Plural': 'anen',
        'S2_Plural': 'anen',
        'S3_Plural': 'anen'
      },
      pz: {
        'S1_Singular': 'asere',
        'S2_Singular': 'asere',
        'S3_Singular': 'asere',
        'S1_Plural': 'anere',
        'S2_Plural': 'anere',
        'S3_Plural': 'anere'
      },
      ho: {
        'S1_Singular': 'asinon',
        'S2_Singular': 'asinon',
        'S3_Singular': 'asinon',
        'S1_Plural': 'asinonan',
        'S2_Plural': 'asinonan',
        'S3_Plural': 'asinonan'
      }
    },
  
    pastpro: {
      base: {
        'S1_Singular': 't̆u',
        'S2_Singular': 't̆u',
        'S3_Singular': 't̆u',
        'S1_Plural': 't̆es',
        'S2_Plural': 't̆es',
        'S3_Plural': 't̆es'
      },
      withObject: {
        'S3_Singular': {
          'O1_Plural': 't̆it',
          'O2_Plural': 't̆it'
        },
        'S1_Plural': {
          'O3_Singular': 't̆es',
          'O3_Plural': 't̆es'
        }
      },
      rootEndsWithRs: {
        'S1_Singular': 't̆u',
        'S2_Singular': 't̆u',
        'S3_Singular': 't̆u',
        'S1_Plural': 't̆es',
        'S2_Plural': 't̆es',
        'S3_Plural': 't̆es'
      }
    },
  
    regionalVariations: {
      'PZ': {
        'do': 'dv',
        'go': 'gv',
        'e': 'ey'
      },
      'AŞ': {
        'do': 'dv',
        'go': 'gv'
      },
      'HO': {
        'do': 'dv',
        'go': 'gv'
      }
    }
  };