import { ConjugationBase } from './base';
import { VerbCategory, TenseType } from './types';
import { getPhoneticRules } from './utils/phoneticRules';
import { getPersonalPronouns } from './utils/pronouns';

export class TVEConjugation extends ConjugationBase {
  constructor(verbData) {
    super(verbData.filter(row => row.Category === VerbCategory.TVE));
    this.initializeConstants();
  }

  initializeConstants() {
    this.PREVERBS = [
      'ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 
      'mo', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'mo', 'ǩoǩo'
    ];

    this.SPECIAL_VERBS = {
      NO_OBJECT: ['coxons', 'cozun', 'gyožin'],
      SPECIAL_PREFIXES: ['oxtimu', 'olva', 'oxenu']
    };

    this.SUFFIXES = {
      PRESENT: {
        'S1_Singular': 'r',
        'S2_Singular': 'r',
        'S3_Singular': 'n',
        'S1_Plural': 'rt',
        'S2_Plural': 'rt',
        'S3_Plural': 'nan'
      },
      PAST: {
        'S1_Singular': 'i',
        'S2_Singular': 'i',
        'S3_Singular': 'u',
        'S1_Plural': 'it',
        'S2_Plural': 'it',
        'S3_Plural': 'es' // 'ey' for Ardeshen
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
        HO: {
          'S1_Singular': 'aminon',
          'S2_Singular': 'aginon',
          'S3_Singular': 'asinon',
          'S1_Plural': 'atminonan',
          'S2_Plural': 'atginonan',
          'S3_Plural': 'asinonan'
        }
      },
      PAST_PROGRESSIVE: {
        'S1_Singular': 'rt̆i',
        'S2_Singular': 'rt̆i',
        'S3_Singular': 'rt̆u',
        'S1_Plural': 'rt̆it',
        'S2_Plural': 'rt̆it',
        'S3_Plural': 'rt̆es'
      },
      OPTATIVE: {
        'S1_Singular': 'a',
        'S2_Singular': 'a',
        'S3_Singular': 'as',
        'S1_Plural': 'at',
        'S2_Plural': 'at',
        'S3_Plural': 'an'
      }
    };
  }

  validate(infinitive, subject, obj, options = {}) {
    const { applicative, causative } = options;

    if (this.SPECIAL_VERBS.NO_OBJECT.includes(infinitive) && obj) {
      throw new Error('This verb cannot take an object');
    }

    if (applicative && causative) {
      throw new Error('Cannot have both applicative and causative markers');
    }

    if ((applicative || causative) && !obj) {
      throw new Error(`${applicative ? 'Applicative' : 'Causative'} requires an object`);
    }

    return true;
  }

  determineMarker(subject, obj, markerType) {
    if (markerType === 'applicative') {
      if (['O1_Singular', 'O2_Singular', 'O1_Plural', 'O2_Plural'].includes(obj)) {
        return 'i';
      }
      return obj?.startsWith('O3') ? 'u' : '';
    }

    if (markerType === 'causative') {
      return 'o';
    }

    return '';
  }

  handlePreverb(preverb, subject, obj, root, region) {
    let prefix = '';

    if (['oxo', 'oǩo'].includes(preverb)) {
      if (['O1_Singular', 'O1_Plural', 'O2_Singular', 'O2_Plural'].includes(obj)) {
        prefix = `${preverb}m`;
      } else if (subject.startsWith('S1_')) {
        prefix = `${preverb}v`;
      } else if (subject.startsWith('S2_')) {
        prefix = `${preverb}g`;
      } else {
        prefix = preverb;
      }
    } else if (preverb === 'me') {
      if (obj?.startsWith('O2_')) {
        prefix = 'meg';
      } else if (subject.startsWith('S1_')) {
        prefix = 'mev';
      } else if (obj?.startsWith('O1_')) {
        prefix = 'mom';
      } else {
        prefix = 'me';
      }
    } else if (preverb === 'do') {
      if (['PZ', 'AŞ', 'HO'].includes(region)) {
        root = root.slice(1);
      }
      if (obj?.startsWith('O1_')) {
        prefix = 'dom';
      } else if (subject.startsWith('S1_')) {
        prefix = 'dov';
      } else if (obj?.startsWith('O2_')) {
        prefix = 'dog';
      } else {
        prefix = 'do';
      }
    }

    return { prefix, root };
  }

  handleRootTransformations(root, subject, obj, options = {}) {
    const { applicative, causative } = options;

    if (applicative && causative) {
      if (root.match(/ms|ps$/)) {
        return root.slice(0, -3) + 'ap';
      } else if (root.match(/umers|amers$/)) {
        return root.slice(0, -5) + 'ap';
      } else if (root.endsWith('rs')) {
        return root.slice(0, -1) + 'ap';
      }
    } else if (applicative) {
      if (root.match(/^(işums|işups|idums|itkums|itkups)$/)) {
        return root.slice(0, -3) + 'v';
      } else if (root.match(/ms|ps$/)) {
        return root.slice(0, -3);
      }
    } else if (causative) {
      if (root === 'digurams') {
        return root;
      } else if (root.match(/^(oşums|oşups|odums|otkums|otkups)$/)) {
        return root.slice(0, -3) + 'vap';
      } else if (root.match(/ms|ps$/)) {
        return root.slice(0, -3) + 'ap';
      } else if (root.match(/umers|amers$/)) {
        return root.slice(0, -5) + 'ap';
      } else if (root.endsWith('rs')) {
        return root.slice(0, -1) + 'ap';
      }
    }

    return root;
  }

  handleSpecialCases(infinitive, root, subject, region, tense) {
    if (['oxtimu', 'olva'].includes(infinitive) && 
        ['past', 'future', 'optative'].includes(tense)) {
      return 'id';
    }

    if (infinitive === 'oxenu') {
      if (subject.startsWith('S1_')) {
        return { root: 'ore', prefix: region === 'FA' ? 'b' : '' };
      } else if (subject === 'S2_Singular') {
        return { root: region === 'AŞ' ? '(o)rer' : '(o)re', prefix: '' };
      } else if (subject === 'S3_Singular') {
        return {
          root: ['PZ', 'AŞ'].includes(region) ? 'on' : '(o)ren',
          prefix: ''
        };
      }
    }

    return { root, prefix: '' };
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
        
        // Handle marker
        let marker = '';
        const { applicative, causative } = options;
        if (applicative || causative) {
          marker = this.determineMarker(subject, obj, applicative ? 'applicative' : 'causative');
          root = this.handleMarker(infinitive, root, marker);
        }

        // Handle preverb
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        let prefix = '';
        if (preverb) {
          const { prefix: newPrefix, root: newRoot } = this.handlePreverb(preverb, subject, obj, root, region);
          prefix = newPrefix;
          root = newRoot;
        }

        // Transform root based on markers and rules
        root = this.handleRootTransformations(root, subject, obj, options);

        // Handle special cases
        const specialCase = this.handleSpecialCases(infinitive, root, subject, region, tense);
        if (specialCase.root) {
          root = specialCase.root;
          prefix = specialCase.prefix || prefix;
        }

        // Get suffix based on tense
        let suffix = '';
        switch (tense) {
          case TenseType.PRESENT:
            suffix = this.SUFFIXES.PRESENT[subject];
            break;
          case TenseType.PAST:
            suffix = this.SUFFIXES.PAST[subject];
            if (region === 'AŞ' && subject === 'S3_Plural') {
              suffix = 'ey';
            }
            break;
          case TenseType.FUTURE:
            suffix = region === 'HO' ? 
              this.SUFFIXES.FUTURE.HO[subject] : 
              this.SUFFIXES.FUTURE.BASE[subject];
            break;
          case TenseType.PAST_PROGRESSIVE:
            suffix = this.SUFFIXES.PAST_PROGRESSIVE[subject];
            break;
          case TenseType.OPTATIVE:
            suffix = this.SUFFIXES.OPTATIVE[subject];
            break;
        }

        const conjugatedForm = `${prefix}${root}${suffix}`.trim();
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugateImperative(infinitive, subject, obj = null, options = {}) {
    if (subject !== 'all' && !['S2_Singular', 'S2_Plural'].includes(subject)) {
      throw new Error("Imperatives are only available for S2_Singular, S2_Plural, or 'all'");
    }

    const normalConjugation = this.conjugate(infinitive, TenseType.PRESENT, subject, obj, options);
    const results = {};

    for (const [region, conjugations] of Object.entries(normalConjugation)) {
      results[region] = conjugations.map(([subj, obj, form]) => {
        // Strip present tense markers and add imperative form
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