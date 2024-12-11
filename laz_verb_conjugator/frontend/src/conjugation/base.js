export class ConjugationBase {
    constructor(verbData) {
      this.verbs = new Map();
      this.regions = new Map();
      this.loadVerbData(verbData);
      this.initializeConstants();
    }
  
    initializeConstants() {
      this.INVALID_COMBINATIONS = new Set([
        'S1_Singular-O1_Singular', 
        'S1_Singular-O1_Plural',
        'S1_Plural-O1_Singular', 
        'S1_Plural-O1_Plural',
        'S2_Singular-O2_Singular', 
        'S2_Singular-O2_Plural',
        'S2_Plural-O2_Singular', 
        'S2_Plural-O2_Plural'
      ]);
  
      this.SPECIAL_VERBS = {
        NO_OBJECT: ['coxons', 'cozun', 'gyožin'],
        SPECIAL_ROOT: ['oxtimu', 'olva', 'oxenu'],
        COMPOUND: ['oǩoreʒxu', 'geç̌ǩu', 'doguru']
      };
  
      this.REGION_SPECIFIC = {
        'PZ': {
          SUFFIXES: {
            FUTURE: {
              'S3_Singular': 'asere',
              'S3_Plural': 'anere'
            }
          },
          PREVERBS: {
            'do': 'dv',
            'go': 'gv',
            'e': 'ey'
          }
        },
        'AŞ': {
          SUFFIXES: {
            PAST: {
              'S3_Plural': 'ey'
            }
          }
        }
      };
    }
  
    loadVerbData(verbData) {
      for (const row of verbData) {
        const infinitive = row['Laz Infinitive'];
        const presentForms = [
          [row['Laz 3rd Person Singular Present'], row['Region']],
          [row['Laz 3rd Person Singular Present Alternative 1'], row['Region Alternative 1']],
          [row['Laz 3rd Person Singular Present Alternative 2'], row['Region Alternative 2']]
        ].filter(([form]) => form);
  
        const regions = [row['Region'], row['Region Alternative 1'], row['Region Alternative 2']]
          .filter(Boolean)
          .flatMap(r => r.split(',').map(s => s.trim()));
  
        this.verbs.set(infinitive, presentForms);
        this.regions.set(infinitive, regions.length ? regions : ['All']);
      }
    }
  
    validateInput(subject, obj, options = {}) {
      const { applicative, causative } = options;
      
      // Check SxOx combinations
      if (obj && this.INVALID_COMBINATIONS.has(`${subject}-${obj}`)) {
        throw new Error('Invalid subject-object combination');
      }
  
      // Check marker requirements
      if ((applicative || causative) && !obj) {
        throw new Error(`${applicative ? 'Applicative' : 'Causative'} requires an object`);
      }
  
      // Check special verbs
      if (this.SPECIAL_VERBS.NO_OBJECT.includes(this.currentVerb) && obj) {
        throw new Error('This verb cannot take an object');
      }
  
      return true;
    }
  
    processCompoundVerb(verb) {
      if (!verb) return '';
      
      const parts = verb.split(' ');
      if (parts.length <= 1) return verb;
  
      return {
        firstWord: parts[0],
        root: parts.slice(1).join(' '),
        isCompound: true
      };
    }
  
    handlePhoneticRules(root, prefix, region) {
      const firstLetter = this.getFirstLetter(root);
      const rules = this.getPhoneticRules(region);
  
      // Handle vowel harmony
      if (this.isVowel(prefix.slice(-1)) && this.isVowel(firstLetter)) {
        prefix = prefix.slice(0, -1);
      }
  
      // Apply consonant rules
      for (const [result, triggers] of Object.entries(rules)) {
        if (triggers.includes(firstLetter)) {
          return result;
        }
      }
  
      return prefix;
    }
  
    handleMarkerSystem(root, options = {}) {
      const { applicative, causative, subject, obj } = options;
  
      if (applicative && causative) {
        throw new Error('Cannot have both applicative and causative markers');
      }
  
      let marker = '';
      if (applicative) {
        marker = this.getApplicativeMarker(subject, obj);
      } else if (causative) {
        marker = 'o';
      }
  
      return this.applyMarker(root, marker);
    }
  
    getApplicativeMarker(subject, obj) {
      if (obj?.startsWith('O3')) return 'u';
      if (['O1', 'O2'].some(prefix => obj?.startsWith(prefix))) return 'i';
      return '';
    }
  
    applyMarker(root, marker) {
      if (!marker) return root;
  
      // Handle special cases first
      if (this.SPECIAL_VERBS.COMPOUND.includes(this.currentVerb)) {
        return this.handleSpecialMarkerCases(root, marker);
      }
  
      // Standard marker application
      if (root.startsWith('i') || root.startsWith('o')) {
        return marker + root.slice(1);
      }
  
      return marker + root;
    }
  
    handleRegionalVariations(conjugation, region) {
      const regionalRules = this.REGION_SPECIFIC[region];
      if (!regionalRules) return conjugation;
  
      let modified = conjugation;
  
      // Apply suffix variations
      if (regionalRules.SUFFIXES?.[this.currentTense]?.[this.currentSubject]) {
        const newSuffix = regionalRules.SUFFIXES[this.currentTense][this.currentSubject];
        modified = modified.replace(/[a-z]+$/, newSuffix);
      }
  
      // Apply preverb variations
      for (const [preverb, replacement] of Object.entries(regionalRules.PREVERBS || {})) {
        if (modified.startsWith(preverb)) {
          modified = modified.replace(preverb, replacement);
        }
      }
  
      return modified;
    }
  
    handleSpecialCases(root, options = {}) {
      const { subject, region, tense } = options;
  
      // Special verb handling
      if (this.SPECIAL_VERBS.SPECIAL_ROOT.includes(this.currentVerb)) {
        return this.handleSpecialVerbCases(root, subject, region, tense);
      }
  
      // Compound verb handling
      if (this.SPECIAL_VERBS.COMPOUND.includes(this.currentVerb)) {
        return this.handleCompoundVerbCases(root, options);
      }
  
      return root;
    }
  
    conjugate(infinitive, tense, subject, obj = null, options = {}) {
      // Store current context
      this.currentVerb = infinitive;
      this.currentTense = tense;
      this.currentSubject = subject;
  
      // Validate input
      this.validateInput(subject, obj, options);
  
      // Get verb forms
      const verbForms = this.verbs.get(infinitive);
      if (!verbForms) {
        throw new Error(`Verb ${infinitive} not found`);
      }
  
      const results = {};
  
      for (const [form, regionStr] of verbForms) {
        const regions = regionStr.split(',').map(r => r.trim());
        
        for (const region of regions) {
          if (!results[region]) {
            results[region] = [];
          }
  
          // Process verb
          const processed = this.processCompoundVerb(form);
          let root = processed.root || processed;
          const firstWord = processed.firstWord || '';
  
          // Apply markers
          root = this.handleMarkerSystem(root, { ...options, subject, obj });
  
          // Handle special cases
          root = this.handleSpecialCases(root, { subject, region, tense });
  
          // Get appropriate suffix
          const suffix = this.getSuffix(tense, subject, obj, region);
  
          // Build conjugated form
          let conjugated = `${root}${suffix}`;
          
          // Apply regional variations
          conjugated = this.handleRegionalVariations(conjugated, region);
  
          // Add first word back if compound
          if (firstWord) {
            conjugated = `${firstWord} ${conjugated}`;
          }
  
          results[region].push([subject, obj, conjugated.trim()]);
        }
      }
  
      return results;
    }
    handlePastProgressiveSuffix(subject, root, region) {
    const basicSuffix = {
        'S1_Singular': 'rt̆i',
        'S2_Singular': 'rt̆i',
        'S3_Singular': 'rt̆u',
        'S1_Plural': 'rt̆it',
        'S2_Plural': 'rt̆it',
        'S3_Plural': 'rt̆es'
    };

    const rootEndsWithRsSuffix = {
        'S1_Singular': 't̆i',
        'S2_Singular': 't̆i',
        'S3_Singular': 't̆u',
        'S1_Plural': 't̆it',
        'S2_Plural': 't̆it',
        'S3_Plural': 't̆es'
    };

    // Handle regional variations
    if (region === 'AŞ' && subject === 'S3_Plural') {
        basicSuffix['S3_Plural'] = 'rt̆ey';
        rootEndsWithRsSuffix['S3_Plural'] = 't̆ey';
    }

    return root.endsWith('rs') ? rootEndsWithRsSuffix[subject] : basicSuffix[subject];
    }

    handlePastProgressiveRoot(root, options = {}) {
    const { applicative, causative } = options;
    
    if (applicative && causative) {
        if (root.endsWith('rs')) {
        return root.slice(0, -1) + 'apam';
        }
        if (root.match(/ms|ps$/)) {
        return root.slice(0, -3) + 'apam';
        }
        if (root.match(/umers|amers$/)) {
        return root.slice(0, -5) + 'apam';
        }
    } else if (applicative) {
        if (root.match(/ms|ps$/)) {
        return root.slice(0, -3);
        }
    } else if (causative) {
        if (root === 'digurams') {
        return root;
        }
        if (root.endsWith('rs')) {
        return root.slice(0, -1) + 'apam';
        }
        if (root.match(/ms|ps$/)) {
        return root.slice(0, -3) + 'apam';
        }
    }

    // Handle base case
    if (root.endsWith('en')) {
        return root.slice(0, -1);
    }
    if (root.endsWith('s')) {
        return root.slice(0, -1);
    }
    
    return root;
    }
  
    // Helper methods
    isVowel(char) {
      return /[aeiou]/i.test(char);
    }
  
    getFirstLetter(word) {
      if (word.length > 1 && ['t̆', 'ç̌', 'ǩ', 'p̌'].includes(word.slice(0, 2))) {
        return word.slice(0, 2);
      }
      return word[0];
    }
  }