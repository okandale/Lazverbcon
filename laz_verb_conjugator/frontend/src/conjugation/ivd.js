import { ConjugationBase } from './base';
import { VerbCategory, TenseType } from './types';
import { PreverbRules } from './utils/preverbs';
import { IVDSuffixes } from './utils/suffixes';
import { getPhoneticRules } from './utils/phoneticRules';

export class IVDConjugation extends ConjugationBase {
  constructor(verbData) {
    super(verbData.filter(row => row.Category === VerbCategory.IVD));
    this.preverbs = PreverbRules;
    this.suffixes = IVDSuffixes;
    this.initializeSuffixes();
  }

  initializeSuffixes() {
    this.SUFFIXES = {
      PRESENT: {
        'S1_Singular': '',
        'S2_Singular': '',
        'S3_Singular': '',
        'S1_Plural': 'an',
        'S2_Plural': 'an',
        'S3_Plural': 'an'
      },
      PAST: {
        'S1_Singular': 'i',
        'S2_Singular': 'i',
        'S3_Singular': 'u',
        'S1_Plural': 'it',
        'S2_Plural': 'it',
        'S3_Plural': 'es'  // 'ey' for Ardesheni
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
          'S1_Plural': 'atminonan',
          'S2_Plural': 'atginonan',
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
        },
        ROOT_ENDS_WITH_RS: {
          'S1_Singular': 't̆i',
          'S2_Singular': 't̆i',
          'S3_Singular': 't̆u',
          'S1_Plural': 't̆it',
          'S2_Plural': 't̆it',
          'S3_Plural': 't̆es'
        }
      },
      IMPERATIVE: {
        'S2_Singular': '',
        'S2_Plural': 'it'
      }
    };
  }

  getPreverb(infinitive) {
    const mainInfinitive = this.processCompoundVerb(infinitive);
    
    // Check each preverb group
    for (const [groupName, preverbs] of Object.entries(this.preverbs.groups)) {
      for (const preverb of preverbs) {
        if (mainInfinitive.startsWith(preverb)) {
          return {
            preverb,
            group: groupName,
            modifiers: this.preverbs.modifiers[groupName]
          };
        }
      }
    }
    
    return null;
  }

  handleSpecialCaseU(root, subject, preverb) {
    // Handle verbs starting with 'u'
    if (root.startsWith('u')) {
      if (['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
        root = 'i' + root.slice(1);
      }
    }

    // Handle verbs with 'i' in root when preverb is 'd'
    if (preverb === 'd') {
      const firstVowelIndex = Array.from(root).findIndex(char => 'aeiou'.includes(char));
      if (firstVowelIndex !== -1 && root[firstVowelIndex] === 'i') {
        if (['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
          root = root.slice(0, firstVowelIndex) + 'a' + root.slice(firstVowelIndex + 1);
        }
      }
    }

    return root;
  }

  handleSpecialPreverbs(root, subject, preverbInfo) {
    if (!preverbInfo) return root;
    const { preverb } = preverbInfo;

    // Handle 'coz' preverb
    if (preverb === 'coz') {
      return 'ozun';
    }

    // Handle 'gy' preverb
    if (preverb === 'gy' && 
        ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
      return root[0] + root.slice(2);
    }

    // Handle 'go' preverb
    if (preverb === 'go' && !subject.startsWith('S3_')) {
      return root.slice(2);
    }

    return root;
  }

  handleCompoundWord(verb) {
    const parts = verb.split(' ');
    if (parts.length <= 1) return { firstWord: '', mainPart: verb };
    return {
      firstWord: parts[0],
      mainPart: parts.slice(1).join(' ')
    };
  }

  conjugatePresent(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    // Validate verb exists
    if (!this.verbs.has(infinitive)) {
      return { error: `Infinitive ${infinitive} not found` };
    }

    // Get verb forms and regions
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
        const phoneticRules = getPhoneticRules(region);
        
        // Handle preverb if exists
        const preverbInfo = this.getPreverb(infinitive);
        let prefix = '';

        if (preverbInfo) {
          const { preverb, modifiers } = preverbInfo;
          prefix = modifiers[subject] || '';
          root = root.slice(preverb.length);
          
          // Apply special preverb handling
          root = this.handleSpecialPreverbs(root, subject, preverbInfo);
        }

        // Handle special cases
        root = this.handleSpecialCaseU(root, subject, prefix);

        // Get appropriate suffix
        let suffix = this.SUFFIXES.PRESENT[subject];
        if (obj) {
          suffix = this.suffixes.present.withObject?.[subject]?.[obj] || suffix;
        }

        // Build conjugated form
        const conjugatedForm = firstWord ? 
          `${firstWord} ${prefix}${root}${suffix}` : 
          `${prefix}${root}${suffix}`.trim();
        
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugatePast(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    if (!this.verbs.has(infinitive)) {
      return { error: `Infinitive ${infinitive} not found` };
    }

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
        const preverbInfo = this.getPreverb(infinitive);
        let prefix = '';
        
        if (preverbInfo) {
          const { preverb, modifiers } = preverbInfo;
          prefix = modifiers[subject] || '';
          root = root.slice(preverb.length);
          root = this.handleSpecialPreverbs(root, subject, preverbInfo);
        }

        root = this.handleSpecialCaseU(root, subject, prefix);

        // Get appropriate suffix
        let suffix = this.SUFFIXES.PAST[subject];
        if (region === 'AŞ' && subject === 'S3_Plural') {
          suffix = 'ey';
        }
        if (obj) {
          suffix = this.suffixes.past.withObject?.[subject]?.[obj] || suffix;
        }

        if (root.endsWith('rs')) {
          root = root.slice(0, -1);
        }

        const conjugatedForm = firstWord ? 
          `${firstWord} ${prefix}${root}${suffix}` : 
          `${prefix}${root}${suffix}`.trim();
          
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugateFuture(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    if (!this.verbs.has(infinitive)) {
      return { error: `Infinitive ${infinitive} not found` };
    }

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
        const preverbInfo = this.getPreverb(infinitive);
        let prefix = '';

        if (preverbInfo) {
          const { preverb, modifiers } = preverbInfo;
          prefix = modifiers[subject] || '';
          root = root.slice(preverb.length);
          root = this.handleSpecialPreverbs(root, subject, preverbInfo);
        }

        root = this.handleSpecialCaseU(root, subject, prefix);

        // Special cases
        if (this.suffixes.special[infinitive]) {
          root = root.slice(0, -1) + this.suffixes.special[infinitive];
        }

        // Get appropriate suffix based on region
        let suffix;
        if (region === 'PZ') {
          suffix = this.SUFFIXES.FUTURE.PZ[subject];
        } else if (region === 'HO') {
          suffix = this.SUFFIXES.FUTURE.HO[subject];
        } else {
          suffix = this.SUFFIXES.FUTURE.BASE[subject];
        }

        if (root.endsWith('rs') || root.endsWith('s')) {
          root = root.slice(0, -1);
        }

        const conjugatedForm = firstWord ? 
          `${firstWord} ${prefix}${root}${suffix}` : 
          `${prefix}${root}${suffix}`.trim();
          
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugatePastProgressive(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    if (!this.verbs.has(infinitive)) {
      return { error: `Infinitive ${infinitive} not found` };
    }

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
        const preverbInfo = this.getPreverb(infinitive);
        let prefix = '';

        if (preverbInfo) {
          const { preverb, modifiers } = preverbInfo;
          prefix = modifiers[subject] || '';
          root = root.slice(preverb.length);
          root = this.handleSpecialPreverbs(root, subject, preverbInfo);
        }

        root = this.handleSpecialCaseU(root, subject, prefix);

        // Get appropriate suffix
        let suffix;
        if (root.endsWith('rs')) {
          suffix = this.SUFFIXES.PAST_PROGRESSIVE.ROOT_ENDS_WITH_RS[subject];
          root = root.slice(0, -1);
        } else {
          suffix = this.SUFFIXES.PAST_PROGRESSIVE.BASE[subject];
          if (obj) {
            suffix = this.suffixes.pastpro.withObject?.[subject]?.[obj] || suffix;
          }
        }

        const conjugatedForm = firstWord ? 
          `${firstWord} ${prefix}${root}${suffix}` : 
          `${prefix}${root}${suffix}`.trim();
          
        results[region].push([subject, obj, conjugatedForm]);
      }
    }

    return results;
  }

  conjugateImperative(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    // Validate subject is either S2_Singular, S2_Plural, or 'all'
    if (subject !== 'all' && !['S2_Singular', 'S2_Plural'].includes(subject)) {
      return { error: "Imperatives are only available for S2_Singular, S2_Plural, or 'all'" };
    }

    if (!this.verbs.has(infinitive)) {
      return { error: `Infinitive ${infinitive} not found` };
    }

    const verbForms = this.verbs.get(infinitive);
    const results = {};
    const subjects = subject === 'all' ? ['S2_Singular', 'S2_Plural'] : [subject];

    for (const [thirdPerson, regionStr] of verbForms) {
      const regions = regionStr.split(',').map(r => r.trim());
      
      for (const region of regions) {
        if (!results[region]) {
          results[region] = [];
        }

        for (const currentSubject of subjects) {
          let root = this.processCompoundVerb(thirdPerson);
          const firstWord = root.firstWord || '';
          root = root.root || root;
          const preverbInfo = this.getPreverb(infinitive);
          let prefix = '';

          if (preverbInfo) {
            const { preverb, modifiers } = preverbInfo;
            prefix = modifiers[currentSubject] || '';
            root = root.slice(preverb.length);
            root = this.handleSpecialPreverbs(root, currentSubject, preverbInfo);
          }

          root = this.handleSpecialCaseU(root, currentSubject, prefix);

          // Special handling for imperative forms
          if (root.endsWith('rs') || root.endsWith('s')) {
            root = root.slice(0, -1);
          }

          // Remove present tense markers and add imperative suffix
          const base = root.replace(/[rtn]$/, '');
          const suffix = this.SUFFIXES.IMPERATIVE[currentSubject];

          const conjugatedForm = firstWord ? 
            `${firstWord} ${prefix}${base}${suffix}` : 
            `${prefix}${base}${suffix}`.trim();
            
          results[region].push([currentSubject, obj, conjugatedForm]);
        }
      }
    }

    return results;
  }

  conjugateNegativeImperative(infinitive, subject, obj = null, options = {}) {
    const { applicative = false, causative = false, useOptionalPreverb = false } = options;
    
    // Get regular imperative forms first
    const imperativeResults = this.conjugateImperative(infinitive, subject, obj, options);
    
    if (imperativeResults.error) {
      return imperativeResults;
    }

    // Transform results to negative form
    const results = {};
    
    for (const [region, conjugations] of Object.entries(imperativeResults)) {
      results[region] = conjugations.map(([subj, obj, form]) => {
        // Add negative prefix 'mo' for HO region, 'mot' for others
        const negPrefix = region === 'HO' ? 'mo' : 'mot';
        return [subj, obj, `${negPrefix} ${form}`];
      });
    }

    return results;
  }

  handleOptionalPreverb(prefix, subject, options) {
    if (!options.useOptionalPreverb) return prefix;
    
    if (!prefix) {
      return ['O3_Singular', 'O3_Plural'].includes(subject) ? 'k' : 'ko' + prefix;
    }
    return prefix;
  }

  handleApplicativeCausative(root, options = {}) {
    const { applicative, causative } = options;
    
    if (applicative && causative) {
      throw new Error("A verb can either have an applicative marker or a causative marker, but not both.");
    }

    if (applicative) {
      // Add applicative marker based on root type
      if (root.endsWith('rs')) {
        return root.slice(0, -2) + 'ap';
      }
      return root + 'ap';
    }

    if (causative) {
      // Add causative marker based on root type
      if (root.endsWith('rs')) {
        return root.slice(0, -2) + 'ap';
      }
      return root + 'op';
    }

    return root;
  }

  conjugate(infinitive, tense, subject, obj = null, options = {}) {
    switch (tense) {
      case TenseType.PRESENT:
        return this.conjugatePresent(infinitive, subject, obj, options);
      case TenseType.PAST:
        return this.conjugatePast(infinitive, subject, obj, options);
      case TenseType.FUTURE:
        return this.conjugateFuture(infinitive, subject, obj, options);
      case TenseType.PAST_PROGRESSIVE:
        return this.conjugatePastProgressive(infinitive, subject, obj, options);
      case TenseType.IMPERATIVE:
        return this.conjugateImperative(infinitive, subject, obj, options);
      default:
        throw new Error(`Unsupported tense: ${tense}`);
    }
  }
}