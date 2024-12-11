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
    this.PREVERBS = [
      'ge', 'e', 'ce', 'dolo', 'do', 'oxo', 'me', 'go', 'oǩo', 'gama', 
      'mo', 'ye'
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
      }
    };
  }

  validate(infinitive, subject, obj, options = {}) {
    const { passive } = options;

    if (passive && obj) {
      throw new Error('Passive form cannot have an object');
    }

    return true;
  }

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

        // Add passive marker
        root = 'i' + root;

        // Transform root based on tense
        if (root.endsWith('en')) {
          root = root.slice(0, -2);
        }
        if (root.endsWith('s')) {
          root = root.slice(0, -1);
        }

        // Get appropriate suffix
        const suffixSet = causative ? 
          this.PASSIVE_SUFFIXES[tense].CAUSATIVE : 
          this.PASSIVE_SUFFIXES[tense].BASE;

        const conjugatedForm = `${preverb || ''}${root}${suffixSet[subject]}`.trim();
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

        // Handle preverb
        const preverb = this.PREVERBS.find(p => root.startsWith(p));
        if (preverb) {
          root = root.slice(preverb.length);
        }

        // Special handling for specific verbs
        if (root === 'geçamu') {
          root = 'geçu';
        } else if (root === 'ceçamu') {
          root = 'ceçu';
        }

        // Handle gama/gam preverb specially
        if (preverb === 'gama' || preverb === 'gam') {
          root = 'ç';
          const prefix = subject.startsWith('S3_') ? 'gam' : 'gamo';
          root = prefix + root;
        }

        // Get appropriate suffix
        let suffix;
        if (tense === TenseType.FUTURE) {
          suffix = region === 'HO' ? 
            this.POTENTIAL_SUFFIXES.FUTURE.HO[subject] : 
            this.POTENTIAL_SUFFIXES.FUTURE.BASE[subject];
        } else {
          suffix = this.POTENTIAL_SUFFIXES.PRESENT[subject];
        }

        const conjugatedForm = `${preverb || ''}${root}${suffix}`.trim();
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

        const conjugatedForm = `${prefix}${root}${suffix}`.trim();
        results[region].push([subject, null, conjugatedForm]);
      }
    }

    return results;
  }

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
}