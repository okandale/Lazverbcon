export const Suffixes = {
    IVD: {
      present: {
        base: {
          'S1_Singular': '',
          'S2_Singular': '',
          'S3_Singular': '',
          'S1_Plural': 'an',
          'S2_Plural': 'an',
          'S3_Plural': 'an'
        },
        withObject: {
          'S3_Singular': {
            'O3_Singular': '',
            'O3_Plural': 'an',
            'O1_Plural': 'rt',
            'O2_Plural': 'rt'
          }
        }
      }
    },
  
    TVE: {
      present: {
        base: {
          'S1_Singular': 'r',
          'S2_Singular': 'r',
          'S3_Singular': 'n',
          'S1_Plural': 'rt',
          'S2_Plural': 'rt',
          'S3_Plural': 'nan'
        }
      },
      past: {
        base: {
          'S1_Singular': 'i',
          'S2_Singular': 'i',
          'S3_Singular': 'u',
          'S1_Plural': 'it',
          'S2_Plural': 'it',
          'S3_Plural': 'es'  // 'ey' for AŞ
        }
      },
      future: {
        base: {
          'S1_Singular': 'are',
          'S2_Singular': 'are',
          'S3_Singular': 'asen',
          'S1_Plural': 'aten',
          'S2_Plural': 'aten',
          'S3_Plural': 'anen'
        },
        ho: {
          'S1_Singular': 'aminon',
          'S2_Singular': 'aginon',
          'S3_Singular': 'asinon',
          'S1_Plural': 'atminonan',
          'S2_Plural': 'atginonan',
          'S3_Plural': 'asinonan'
        }
      }
    },
  
    TVM: {
      present: {
        base: {
          'S1_Singular': 'r',
          'S2_Singular': 'r',
          'S3_Singular': 'n',
          'S1_Plural': 'rt',
          'S2_Plural': 'rt',
          'S3_Plural': 'nan'
        }
      }
    },
  
    Combined: {
      passive: {
        present: {
          'S1_Singular': 'er',
          'S2_Singular': 'er',
          'S3_Singular': 'en',
          'S1_Plural': 'ert',
          'S2_Plural': 'ert',
          'S3_Plural': 'enan'
        },
        causative: {
          'S1_Singular': 'apiner',
          'S2_Singular': 'apiner',
          'S3_Singular': 'apinen',
          'S1_Plural': 'apinert',
          'S2_Plural': 'apinert',
          'S3_Plural': 'apinenan'
        }
      },
      potential: {
        present: {
          'S1_Singular': 'en',
          'S2_Singular': 'en',
          'S3_Singular': 'en',
          'S1_Plural': 'enan',
          'S2_Plural': 'enan',
          'S3_Plural': 'enan'
        }
      },
      presentPerfect: {
        fa: {
          'S1_Singular': 'un',
          'S2_Singular': 'un',
          'S3_Singular': 'un',
          'S1_Plural': 'unan',
          'S2_Plural': 'unan',
          'S3_Plural': 'unan'
        },
        other: {
          'S1_Singular': 'apun',
          'S2_Singular': 'apun',
          'S3_Singular': 'apun',
          'S1_Plural': 'apunan',
          'S2_Plural': 'apunan',
          'S3_Plural': 'apunan'
        }
      }
    }
  };