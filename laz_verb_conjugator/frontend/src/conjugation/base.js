import { getPhoneticRules } from './utils/phoneticRules';
import { getPersonalPronouns } from './utils/pronouns';

export class ConjugationBase {
  constructor(verbData) {
    this.verbs = new Map();
    this.regions = new Map();
    this.loadVerbData(verbData);
  }

  loadVerbData(verbData) {
    verbData.forEach(row => {
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
    });
  }

  processCompoundVerb(verb) {
    const parts = verb.split(' ');
    return parts.length > 1 ? parts.slice(1).join(' ') : verb;
  }

  getFirstLetter(root) {
    if (root.length > 1 && ['t̆', 'ç̌', 'ǩ', 'p̌', 'ǯ'].includes(root.slice(0, 2))) {
      return root.slice(0, 2);
    }
    return root[0];
  }

  adjustPrefix(prefix, firstLetter, phoneticRules) {
    for (const [p, letters] of Object.entries(phoneticRules)) {
      if (letters.includes(firstLetter)) {
        return p;
      }
    }
    return prefix;
  }

  validateInput(subject, obj) {
    if ((subject.startsWith('S1_') && obj?.startsWith('O1_')) ||
        (subject.startsWith('S2_') && obj?.startsWith('O2_'))) {
      return false;
    }
    return true;
  }

  conjugate(infinitive, tense, subject, obj = null, options = {}) {
    throw new Error('Must be implemented by child class');
  }
}
