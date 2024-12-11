  // src/conjugation/ivd.js
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
      if (root.startsWith('u')) {
        if (['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
          root = 'i' + root.slice(1);
        }
      }
  
      if (preverb === 'd') {
        const firstVowelIndex = root.split('').findIndex(char => 'aeiou'.includes(char));
        if (firstVowelIndex !== -1 && root[firstVowelIndex] === 'i') {
          if (['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
            root = root.slice(0, firstVowelIndex) + 'a' + root.slice(firstVowelIndex + 1);
          }
        }
      }
  
      return root;
    }
  
    conjugatePresent(infinitive, subject, obj = null, options = {}) {
      const { applicative = false, causative = false, useOptionalPreverb = false } = options;
      
      // Validate verb exists
      if (!this.verbs.has(infinitive)) {
        return { error: `Infinitive ${infinitive} not found` };
      }
  
      // Get verb forms and regions
      const verbForms = this.verbs.get(infinitive);
      const verbRegions = this.regions.get(infinitive);
      const results = {};
  
      for (const [thirdPerson, regionStr] of verbForms) {
        const regions = regionStr.split(',').map(r => r.trim());
        
        for (const region of regions) {
          if (!results[region]) {
            results[region] = [];
          }
  
          // Initialize conjugation components
          let root = this.processCompoundVerb(thirdPerson);
          const firstWord = this.getFirstLetter(root);
          const phoneticRules = getPhoneticRules(region);
          
          // Handle preverb if exists
          const preverbInfo = this.getPreverb(infinitive);
          let prefix = '';
          let suffix = '';
  
          if (preverbInfo) {
            const { preverb, modifiers } = preverbInfo;
            prefix = modifiers[subject] || '';
            root = root.slice(preverb.length);
          }
  
          // Handle special cases
          root = this.handleSpecialCaseU(root, subject, prefix);
  
          // Get appropriate suffix
          if (obj) {
            suffix = this.suffixes.present.withObject[subject]?.[obj] || 
                    this.suffixes.present.base[subject];
          } else {
            suffix = this.suffixes.present.base[subject];
          }
  
          // Build conjugated form
          const conjugatedForm = `${prefix}${root}${suffix}`.trim();
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
          const preverbInfo = this.getPreverb(infinitive);
          let prefix = '';
          
          if (preverbInfo) {
            const { preverb, modifiers } = preverbInfo;
            prefix = modifiers[subject] || '';
            root = root.slice(preverb.length);
          }
  
          root = this.handleSpecialCaseU(root, subject, prefix);
  
          // Get appropriate suffix
          let suffix = this.suffixes.past.base[subject];
          if (obj) {
            suffix = this.suffixes.past.withObject[subject]?.[obj] || suffix;
          }
  
          if (root.endsWith('rs')) {
            root = root.slice(0, -1);
          }
  
          const conjugatedForm = `${prefix}${root}${suffix}`.trim();
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
          const preverbInfo = this.getPreverb(infinitive);
          let prefix = '';
  
          if (preverbInfo) {
            const { preverb, modifiers } = preverbInfo;
            prefix = modifiers[subject] || '';
            root = root.slice(preverb.length);
          }
  
          root = this.handleSpecialCaseU(root, subject, prefix);
  
          // Special cases
          if (this.suffixes.special[infinitive]) {
            root = root.slice(0, -1) + this.suffixes.special[infinitive];
          }
  
          // Get appropriate suffix based on region
          let suffix;
          if (region === 'PZ') {
            suffix = this.suffixes.future.pz[subject];
          } else if (region === 'HO') {
            suffix = this.suffixes.future.ho[subject];
          } else {
            suffix = this.suffixes.future.base[subject];
          }
  
          if (root.endsWith('rs') || root.endsWith('s')) {
            root = root.slice(0, -1);
          }
  
          const conjugatedForm = `${prefix}${root}${suffix}`.trim();
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
          const preverbInfo = this.getPreverb(infinitive);
          let prefix = '';
  
          if (preverbInfo) {
            const { preverb, modifiers } = preverbInfo;
            prefix = modifiers[subject] || '';
            root = root.slice(preverb.length);
          }
  
          root = this.handleSpecialCaseU(root, subject, prefix);
  
          // Get appropriate suffix
          let suffix;
          if (root.endsWith('rs')) {
            suffix = this.suffixes.pastpro.rootEndsWithRs[subject];
            root = root.slice(0, -1);
          } else {
            suffix = this.suffixes.pastpro.base[subject];
            if (obj) {
              suffix = this.suffixes.pastpro.withObject[subject]?.[obj] || suffix;
            }
          }
  
          const conjugatedForm = `${prefix}${root}${suffix}`.trim();
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
            const preverbInfo = this.getPreverb(infinitive);
            let prefix = '';
  
            if (preverbInfo) {
              const { preverb, modifiers } = preverbInfo;
              prefix = modifiers[currentSubject] || '';
              root = root.slice(preverb.length);
            }
  
            root = this.handleSpecialCaseU(root, currentSubject, prefix);
  
            // Special handling for imperative forms
            if (root.endsWith('rs') || root.endsWith('s')) {
              root = root.slice(0, -1);
            }
  
            const suffix = this.suffixes.present.imperative[currentSubject];
            const conjugatedForm = `${prefix}${root}${suffix}`.trim();
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
  
    handleSpecialPreverbs(root, subject, preverbInfo) {
      if (!preverbInfo) return root;
      
      const { preverb } = preverbInfo;
      
      // Special case for 'coz' preverb
      if (preverb === 'coz') {
        return 'ozun';
      }
  
      // Special case for 'gy' preverb
      if (preverb === 'gy' && ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural'].includes(subject)) {
        return root[0] + root.slice(2);
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
  
    conjugateVerb(params) {
      const { 
        infinitive, 
        subject, 
        obj = null, 
        tense = TenseType.PRESENT,
        region,
        root,
        options = {}
      } = params;
  
      // Process compound word
      const { firstWord, mainPart } = this.handleCompoundWord(root);
      
      // Get and process preverb
      const preverbInfo = this.getPreverb(infinitive);
      let processedRoot = mainPart;
      let prefix = '';
  
      if (preverbInfo) {
        const { preverb, modifiers } = preverbInfo;
        prefix = modifiers[subject] || '';
        processedRoot = processedRoot.slice(preverb.length);
      }
  
      // Apply special cases
      processedRoot = this.handleSpecialPreverbs(processedRoot, subject, preverbInfo);
      processedRoot = this.handleSpecialCaseU(processedRoot, subject, prefix);
      
      // Handle optional preverb
      prefix = this.handleOptionalPreverb(prefix, subject, options);
  
      // Handle applicative/causative
      processedRoot = this.handleApplicativeCausative(processedRoot, options);
  
      // Get appropriate suffix based on tense and other factors
      const suffix = this.getSuffix(tense, subject, obj, region, processedRoot);
  
      // Build final form
      const conjugatedForm = `${firstWord} ${prefix}${processedRoot}${suffix}`.trim();
      return conjugatedForm;
    }
  
    getSuffix(tense, subject, obj, region, root) {
      let suffixes;
      
      switch (tense) {
        case TenseType.PRESENT:
          suffixes = this.suffixes.present;
          break;
        case TenseType.PAST:
          suffixes = this.suffixes.past;
          break;
        case TenseType.FUTURE:
          if (region === 'PZ') {
            suffixes = this.suffixes.future.pz;
          } else if (region === 'HO') {
            suffixes = this.suffixes.future.ho;
          } else {
            suffixes = this.suffixes.future.base;
          }
          break;
        case TenseType.PAST_PROGRESSIVE:
          if (root.endsWith('rs')) {
            suffixes = this.suffixes.pastpro.rootEndsWithRs;
          } else {
            suffixes = this.suffixes.pastpro.base;
          }
          break;
        default:
          return '';
      }
  
      if (obj && suffixes.withObject?.[subject]?.[obj]) {
        return suffixes.withObject[subject][obj];
      }
  
      return suffixes.base[subject];
    }
  }