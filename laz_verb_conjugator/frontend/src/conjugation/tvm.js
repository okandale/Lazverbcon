import { ConjugationBase } from './base';
import { VerbCategory, TenseType } from './types';
import { getPhoneticRules } from './utils/phoneticRules';
import { getPersonalPronouns } from './utils/pronouns';

export class TVMConjugation extends ConjugationBase {
  constructor(verbData) {
    super(verbData.filter(row => row.Category === VerbCategory.TVM));
    this.initializeConstants();
  }

  initializeConstants() {
    this.PREVERBS = [
      'ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 
      'mo', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'mo', 'ǩoǩo'
    ];

    this.SUFFIXES = {
      PRESENT: {
        BASE: {
          'S1_Singular': 'r',
          'S2_Singular': 'r',
          'S3_Singular': 'n',
          'S1_Plural': 'rt',
          'S2_Plural': 'rt',
          'S3_Plural': 'nan'
        }
      },
      PAST: {
        BASE: {
          'S1_Singular': 'i',
          'S2_Singular': 'i',
          'S3_Singular': 'u',
          'S1_Plural': 'it',
          'S2_Plural': 'it',
          'S3_Plural': 'es'  // 'ey' for AŞ
        }
      },
      FUTURE: {
        BASE: {
          'S1_Singular': 'are',
          'S2_Singular': 'are',
          'S3_Singular': 'asen',
          'S1_Plural': 'aten',
          'S2_Plural': 'aten',
          'S3_Plural': 'anen'
        },
        PZ: {
          'S1_Singular': 'are',
          'S2_Singular': 'are',
          'S3_Singular': 'asere',
          'S1_Plural': 'atere',
          'S2_Plural': 'atere',
          'S3_Plural': 'anere'
        },
        HO: {
          'S1_Singular': 'aminon',
          'S2_Singular': 'aginon',
          'S3_Singular': 'asinon',
          'S1_Plural': 'aminonan',
          'S2_Plural': 'aginonan',
          'S3_Plural': 'asinonan'
        }
      },
      PAST_PROGRESSIVE: {
        BASE: {
          'S1_Singular': 'rt̆i',
          'S2_Singular': 'rt̆i',
          'S3_Singular': 'rt̆u',
          'S1_Plural': 'rt̆it',
          'S2_Plural': 'rt̆it',
          'S3_Plural': 'rt̆es'
        }
      },
      OPTATIVE: {
        BASE: {
          'S1_Singular': 'a',
          'S2_Singular': 'a',
          'S3_Singular': 'as',
          'S1_Plural': 'at',
          'S2_Plural': 'at',
          'S3_Plural': 'an'
        }
      }
    };

    this.PASSIVE_SUFFIXES = {
      PRESENT: {
        'S1_Singular': 'er',
        'S2_Singular': 'er',
        'S3_Singular': 'en',
        'S1_Plural': 'ert',
        'S2_Plural': 'ert',
        'S3_Plural': 'enan'
      },
      FUTURE: {
        'S1_Singular': 'are',
        'S2_Singular': 'are',
        'S3_Singular': 'asere',
        'S1_Plural': 'atere',
        'S2_Plural': 'atere',
        'S3_Plural': 'anere'
      }
    };

    this.POTENTIAL_SUFFIXES = {
      PRESENT: {
        'S1_Singular': 'en',
        'S2_Singular': 'en',
        'S3_Singular': 'en',
        'S1_Plural': 'enan',
        'S2_Plural': 'enan',
        'S3_Plural': 'enan'
      }
    };
  }

  validate(infinitive, subject, obj, options = {}) {
    const { applicative, causative } = options;

    if (applicative && causative) {
      throw new Error('Cannot have both applicative and causative markers');
    }

    if ((applicative || causative) && !obj) {
      throw new Error(`${applicative ? 'Applicative' : 'Causative'} requires an object`);
    }

    return true;
  }

  handlePreverb(preverb, subject, obj, root, region) {
    if (preverb === 'me' || !preverb) {
      const prefix = this.handleMePreverb(subject, obj, root, region);
      return { prefix, root };
    }

    if (preverb === 'go' && subject.startsWith('S3_') && !obj) {
      return { prefix: '', root };
    }

    let prefix = preverb;
    if (['gama', 'gam'].includes(preverb)) {
      root = 'iç';
      prefix = subject.startsWith('S3_') ? 'gam' : 'gamo';
    }

    return { prefix, root };
  }

  handleMePreverb(subject, obj, root, region) {
    if (obj?.startsWith('O2_')) {
      return 'meg';
    }
    if (subject.startsWith('S1_')) {
      return 'mev';
    }
    if (obj?.startsWith('O1_')) {
      return 'mom';
    }
    return 'n';
  }

  handleMarker(root, marker, options = {}) {
    const { passive, potential } = options;

    if (passive) {
      return 'i' + root;
    }

    if (potential) {
      return marker + root;
    }

    return root;
  }

  handleRootTransformations(root, subject, options = {}) {
    const { tense, passive, potential } = options;

    if (passive) {
      if (root.endsWith('en')) {
        return root.slice(0, -2);
      }
      if (root.endsWith('s')) {
        return root.slice(0, -1);
      }
    }

    if (potential && tense === TenseType.OPTATIVE) {
      if (root.endsWith('ms') || root.endsWith('ps')) {
        return root.slice(0, -3);
      }
      if (root.endsWith('umers') || root.endsWith('amers')) {
        return root.slice(0, -5);
      }
      if (root.endsWith('rs')) {
        return root.slice(0, -1);
      }
    }

    return root;
  }

  handleSpecialCases(infinitive, root, subject, region, tense) {
    if (infinitive === "ren") {
      return this.handleRenConjugation(subject, region, tense);
    }

    return { root, prefix: '' };
  }

  handleRenConjugation(subject, region, tense) {
    if (tense === TenseType.PRESENT) {
      if (subject === 'S1_Singular') {
        return { 
          root: 'ore',
          prefix: region === "FA" ? "b" : ''
        };
      }
      if (subject === 'S2_Singular') {
        return {
          root: region === "AŞ" ? "(o)rer" : "(o)re",
          prefix: ''
        };
      }
      if (subject === 'S3_Singular') {
        return {
          root: ['PZ', 'AŞ'].includes(region) ? 'on' : "(o)ren",
          prefix: ''
        };
      }
    }

    if (['past', 'future'].includes(tense)) {
      return {
        root: 'ort̆',
        prefix: region === "FA" && subject.startsWith('S1_') ? "b" : ''
      };
    }

    return { root: '', prefix: '' };
  }

  conjugate(infinitive, tense, subject, obj = null, options = {}) {
    this.validate(infinitive, subject, obj, options);
    
    const verbForms = this.verbs.get(infinitive);
    const results = {};

    for (const [thirdPerson, regionStr] of verbForms) {
      const regions = regionStr.split(',').map(r => r.trim());
      
      for (const region of regions) {
        if (!results[region]) {
          results[region] = [];
        }

        let root = this.processCompoundVerb(thirdPerson);
        const phoneticRules = getPhoneticRules(region);

        // Handle preverb
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        let { prefix, root: newRoot } = preverb ? 
          this.handlePreverb(preverb, subject, obj, root, region) : 
          { prefix: '', root };
        root = newRoot;

        // Handle markers and transformations
        root = this.handleMarker(root, options.marker || '', options);
        root = this.handleRootTransformations(root, subject, { ...options, tense });

        // Handle special cases
        const specialCase = this.handleSpecialCases(infinitive, root, subject, region, tense);
        if (specialCase.root) {
          root = specialCase.root;
          prefix = specialCase.prefix || prefix;
        }

        // Get appropriate suffix
        let suffix;
        if (options.passive) {
          suffix = this.PASSIVE_SUFFIXES[tense]?.[subject] || 
                  this.PASSIVE_SUFFIXES.PRESENT[subject];
        } else if (options.potential) {
          suffix = this.POTENTIAL_SUFFIXES[tense]?.[subject] || 
                  this.POTENTIAL_SUFFIXES.PRESENT[subject];
        } else {
          const suffixSet = this.SUFFIXES[tense];
          if (region === 'HO' && suffixSet.HO) {
            suffix = suffixSet.HO[subject];
          } else if (region === 'PZ' && suffixSet.PZ) {
            suffix = suffixSet.PZ[subject];
          } else {
            suffix = suffixSet.BASE[subject];
          }

          // Handle Ardeshen dialect
          if (region === 'AŞ' && subject === 'S3_Plural' && tense === TenseType.PAST) {
            suffix = 'ey';
          }
        }

        const conjugatedForm = `${prefix}${root}${suffix}`.trim();
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugatePassive(infinitive, tense, subject, options = {}) {
    return this.conjugate(infinitive, tense, subject, null, { ...options, passive: true });
  }

  conjugatePotential(infinitive, tense, subject, options = {}) {
    return this.conjugate(infinitive, tense, subject, null, { ...options, potential: true });
  }

  conjugateImperative(infinitive, subject, obj = null, options = {}) {
    if (subject !== 'all' && !['S2_Singular', 'S2_Plural'].includes(subject)) {
      throw new Error("Imperatives are only available for S2_Singular, S2_Plural, or 'all'");
    }

    const normalConjugation = this.conjugate(infinitive, TenseType.PRESENT, subject, obj, options);
    const results = {};

    for (const [region, conjugations] of Object.entries(normalConjugation)) {
      results[region] = conjugations.map(([subj, obj, form]) => {
        const root = form.replace(/[rtn]$/, '');
        const suffix = subj === 'S2_Plural' ? 'it' : '';
        return [subj, obj, `${root}${suffix}`];
      });
    }

    return results;
  }

  conjugateNegative(infinitive, tense, subject, obj = null, options = {}) {
    const normalConjugation = this.conjugate(infinitive, tense, subject, obj, options);
    const results = {};

    for (const [region, conjugations] of Object.entries(normalConjugation)) {
      results[region] = conjugations.map(([subj, obj, form]) => {
        const negPrefix = region === 'HO' ? 'va' : 'var';
        return [subj, obj, `${negPrefix} ${form}`];
      });
    }

    return results;
  }
}