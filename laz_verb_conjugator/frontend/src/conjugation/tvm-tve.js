import { ConjugationBase } from './base';
import { VerbCategory, TenseType } from './types';
import { getPhoneticRules } from './utils/phoneticRules';
import { getPersonalPronouns } from './utils/pronouns';

export class TVMTVEConjugation extends ConjugationBase {
  constructor(verbData) {
    super(verbData.filter(row => 
      row.Category === VerbCategory.TVE || row.Category === VerbCategory.TVM
    ));
    this.initializeConstants();
  }

  initializeConstants() {
    // Preverbs for all forms
    this.PREVERBS = [
      'ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 
      'mo', 'ye', 'gela', 'ela', 'ceǩo', 'eǩo', 'ama', 'mo', 'ǩoǩo'
    ];

    // Present Perfect Suffixes
    this.PRESENT_PERFECT_SUFFIXES = {
      FA: {
        'S1_Singular': 'un',
        'S2_Singular': 'un',
        'S3_Singular': 'un',
        'S1_Plural': 'unan',
        'S2_Plural': 'unan',
        'S3_Plural': 'unan'
      },
      OTHER: {
        'S1_Singular': 'apun',
        'S2_Singular': 'apun',
        'S3_Singular': 'apun',
        'S1_Plural': 'apunan',
        'S2_Plural': 'apunan',
        'S3_Plural': 'apunan'
      }
    };

    // Passive Form Suffixes
    this.PASSIVE_SUFFIXES = {
      PRESENT: {
        BASE: {
          'S1_Singular': 'er',
          'S2_Singular': 'er',
          'S3_Singular': 'en',
          'S1_Plural': 'ert',
          'S2_Plural': 'ert',
          'S3_Plural': 'enan'
        },
        CAUSATIVE: {
          'S1_Singular': 'apiner',
          'S2_Singular': 'apiner',
          'S3_Singular': 'apinen',
          'S1_Plural': 'apinert',
          'S2_Plural': 'apinert',
          'S3_Plural': 'apinenan'
        }
      },
      PAST: {
        BASE: {
          'S1_Singular': 'i',
          'S2_Singular': 'i',
          'S3_Singular': 'u',
          'S1_Plural': 'it',
          'S2_Plural': 'it',
          'S3_Plural': 'es'
        },
        CAUSATIVE: {
          'S1_Singular': 'apineri',
          'S2_Singular': 'apineri',
          'S3_Singular': 'apinenu',
          'S1_Plural': 'apinerit',
          'S2_Plural': 'apinerit',
          'S3_Plural': 'apinenanu'
        }
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

    // Potential Form Suffixes
    this.POTENTIAL_SUFFIXES = {
      PRESENT: {
        'S1_Singular': 'en',
        'S2_Singular': 'en',
        'S3_Singular': 'en',
        'S1_Plural': 'enan',
        'S2_Plural': 'enan',
        'S3_Plural': 'enan'
      },
      FUTURE: {
        BASE: {
          'S1_Singular': 'asere',
          'S2_Singular': 'asere',
          'S3_Singular': 'asere',
          'S1_Plural': 'anere',
          'S2_Plural': 'anere',
          'S3_Plural': 'anere'
        },
        HO: {
          'S1_Singular': 'asinon',
          'S2_Singular': 'asinon',
          'S3_Singular': 'asinon',
          'S1_Plural': 'asinonan',
          'S2_Plural': 'asinonan',
          'S3_Plural': 'asinonan'
        }
      },
      OPTATIVE: {
        'S1_Singular': 'as',
        'S2_Singular': 'as',
        'S3_Singular': 'as',
        'S1_Plural': 'an',
        'S2_Plural': 'an',
        'S3_Plural': 'an'
      }
    };
  }

  // Validation methods
  validate(infinitive, subject, obj, options = {}) {
    const { passive, potential } = options;

    if (!this.verbs.has(infinitive)) {
      throw new Error(`Infinitive ${infinitive} not found`);
    }

    if (passive && obj) {
      throw new Error('Passive form cannot have an object');
    }

    if (potential && obj) {
      throw new Error('Potential form cannot have an object');
    }

    return true;
  }

  // Core conjugation methods
  conjugatePassive(infinitive, tense, subject, options = {}) {
    const { causative = false } = options;
    this.validate(infinitive, subject, null, { passive: true });

    const verbForms = this.verbs.get(infinitive);
    const results = {};

    for (const [thirdPerson, regionStr] of verbForms) {
      const regions = regionStr.split(',').map(r => r.trim());
      
      for (const region of regions) {
        if (!results[region]) {
          results[region] = [];
        }

        let root = this.processCompoundVerb(thirdPerson);

        // Handle preverb
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        if (preverb) {
          root = root.slice(preverb.length);
        }

        // Add passive marker and transform root
        root = 'i' + root;
        if (root.endsWith('en')) root = root.slice(0, -2);
        if (root.endsWith('s')) root = root.slice(0, -1);

        // Get appropriate suffix
        const suffixSet = this.PASSIVE_SUFFIXES[tense] || this.PASSIVE_SUFFIXES.PRESENT;
        const suffix = causative ? 
          suffixSet.CAUSATIVE?.[subject] || suffixSet.BASE[subject] : 
          suffixSet.BASE?.[subject] || suffixSet[subject];

        const conjugatedForm = `${preverb || ''}${root}${suffix}`.trim();
        results[region].push([subject, null, conjugatedForm]);
      }
    }

    return results;
  }

  conjugatePotential(infinitive, tense, subject, options = {}) {
    this.validate(infinitive, subject, null, { potential: true });

    const verbForms = this.verbs.get(infinitive);
    const results = {};

    for (const [thirdPerson, regionStr] of verbForms) {
      const regions = regionStr.split(',').map(r => r.trim());
      
      for (const region of regions) {
        if (!results[region]) {
          results[region] = [];
        }

        let root = this.processCompoundVerb(thirdPerson);
        const firstWord = root.firstWord || '';
        root = root.root || root;

        // Handle preverb and special cases
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        if (preverb === 'gama' || preverb === 'gam') {
          root = 'ç';
          const prefix = subject.startsWith('S3_') ? 'gam' : 'gamo';
          root = prefix + root;
        } else if (preverb) {
          root = root.slice(preverb.length);
        }

        // Get appropriate suffix based on tense and region
        let suffix;
        if (tense === TenseType.FUTURE) {
          suffix = region === 'HO' ? 
            this.POTENTIAL_SUFFIXES.FUTURE.HO[subject] : 
            this.POTENTIAL_SUFFIXES.FUTURE.BASE[subject];
        } else if (tense === TenseType.OPTATIVE) {
          suffix = this.POTENTIAL_SUFFIXES.OPTATIVE[subject];
        } else {
          suffix = this.POTENTIAL_SUFFIXES.PRESENT[subject];
        }

        const conjugatedForm = `${firstWord} ${preverb || ''}${root}${suffix}`.trim();
        results[region].push([subject, null, conjugatedForm]);
      }
    }

    return results;
  }

  conjugatePresentPerfect(infinitive, subject, options = {}) {
    this.validate(infinitive, subject, null);

    const verbForms = this.verbs.get(infinitive);
    const results = {};

    for (const [thirdPerson, regionStr] of verbForms) {
      const regions = regionStr.split(',').map(r => r.trim());
      
      for (const region of regions) {
        if (!results[region]) {
          results[region] = [];
        }

        let root = this.processCompoundVerb(thirdPerson);
        const firstWord = root.firstWord || '';
        root = root.root || root;

        // Handle preverb
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        if (preverb) {
          root = root.slice(preverb.length);
        }

        // Add appropriate prefix based on subject
        let prefix = '';
        if (subject.startsWith('S1_')) {
          prefix = 'mi';
        } else if (subject.startsWith('S2_')) {
          prefix = 'gi';
        } else {
          prefix = 'u';
        }

        // Get appropriate suffix based on region
        const suffix = region === 'FA' ? 
          this.PRESENT_PERFECT_SUFFIXES.FA[subject] : 
          this.PRESENT_PERFECT_SUFFIXES.OTHER[subject];

        const conjugatedForm = `${firstWord} ${prefix}${root}${suffix}`.trim();
        results[region].push([subject, null, conjugatedForm]);
      }
    }

    return results;
  }

  // Support methods for handling preverbs and root transformations
  handlePreverbTransformation(preverb, subject, root, region) {
    if (preverb === 'me' || !preverb) {
      const prefix = this.handleMePreverb(subject, root, region);
      return { prefix, root };
    }

    if (preverb === 'gama' || preverb === 'gam') {
      root = 'ç';
      const prefix = subject.startsWith('S3_') ? 'gam' : 'gamo';
      return { prefix, root };
    }

    return { prefix: preverb, root };
  }

  handleMePreverb(subject, root, region) {
    if (subject.startsWith('S1_')) {
      return 'mev';
    }
    if (root.startsWith('n')) {
      return 'n';
    }
    return 'me';
  }

  // Negative form handling
  handleNegative(infinitive, tense, subject, obj = null, options = {}) {
    const { passive, potential } = options;
    let conjugationMethod;

    if (passive) {
      conjugationMethod = this.conjugatePassive.bind(this);
    } else if (potential) {
      conjugationMethod = this.conjugatePotential.bind(this);
    } else {
      conjugationMethod = this.conjugatePresentPerfect.bind(this);
    }

    const normalConjugation = conjugationMethod(infinitive, tense, subject, options);
    const results = {};

    for (const [region, conjugations] of Object.entries(normalConjugation)) {
      results[region] = conjugations.map(([subj, obj, form]) => {
        const negPrefix = region === 'HO' ? 'va' : 'var';
        return [subj, obj, `${negPrefix} ${form}`];
      });
    }

    return results;
  }

  // Error handling
  handleError(error, type = 'validation') {
    console.error(`${type} error:`, error.message);
    throw error;
  }
}