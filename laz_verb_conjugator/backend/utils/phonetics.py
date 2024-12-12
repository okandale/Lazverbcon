from typing import Optional, List, Dict, Tuple, Set
from ..config.verb_rules import VerbRules

class PhoneticProcessor:
    """Utility class for handling phonetic rules and transformations in Laz verb conjugation."""
    
    def __init__(self):
        self._rules = VerbRules()
        self._vowels: Set[str] = set('aeiou')
        self._special_chars: Set[str] = {'t̆', 'ç̌', 'ǩ', 'p̌', 'ǯ'}
        self._compound_markers: Set[str] = {'do', 'mo', 'oko', 'go'}

    def get_first_letter(self, word: str) -> str:
        """
        Get the first letter of a word, handling special characters.
        
        Args:
            word: Input word
            
        Returns:
            First letter or character combination
        """
        if not word:
            return ''
            
        if len(word) > 1 and word[:2] in self._special_chars:
            return word[:2]
            
        # Special case for words starting with 'gy'
        if len(word) > 2 and word.startswith('gy'):
            return word[2:]
            
        return word[0]

    def get_first_vowel_index(self, word: str) -> int:
        """
        Find the index of the first vowel in a word.
        
        Args:
            word: Input word
            
        Returns:
            Index of first vowel or -1 if none found
        """
        for i, char in enumerate(word):
            if char in self._vowels:
                return i
        return -1

    def adjust_prefix(self, prefix: str, first_letter: str, region: str) -> str:
        """
        Adjust a prefix based on phonetic rules for a region.
        
        Args:
            prefix: Original prefix
            first_letter: First letter of following word
            region: Dialect region
            
        Returns:
            Adjusted prefix
        """
        rules = self._rules.get_phonetic_rules(region)
        v_rules = rules.get('v_rules', {})
        
        for target, letters in v_rules.items():
            if first_letter in letters:
                return target
        return prefix

    def handle_special_cases(self, root: str, subject: str, preverb: str) -> str:
        """
        Handle special cases for verb roots.
        
        Args:
            root: The verb root
            subject: Subject marker
            preverb: Preverb (if any)
            
        Returns:
            Modified root
        """
        if not root:
            return root

        # Handle verbs starting with 'u'
        if root.startswith('u'):
            if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                root = 'i' + root[1:]

        # Handle preverb 'd' with 'i' in root
        if preverb == 'd':
            first_vowel_idx = self.get_first_vowel_index(root)
            if first_vowel_idx != -1 and root[first_vowel_idx] == 'i':
                if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                    root = (root[:first_vowel_idx] + 'a' + 
                           root[first_vowel_idx + 1:])

        # Handle special roots
        if root == "diç̌irs":
            root = 'ç̌irs'
        elif root == "dvaç̌irs":
            root = 'ç̌irs'

        return root

    def handle_preverb_combination(self, root: str, preverb: str, 
                                 subject: str, region: str) -> Tuple[str, str, str]:
        """
        Handle combinations of preverbs with roots.
        
        Args:
            root: The verb root
            preverb: The preverb
            subject: Subject marker
            region: Dialect region
            
        Returns:
            Tuple of (modified_root, modified_preverb, prefix)
        """
        if not preverb:
            return root, '', ''

        prefix = ''

        # Special cases for preverbs with vowels
        if (preverb[-1] in self._vowels and 
            root[0] in self._vowels and 
            subject not in ['S1_Singular', 'S1_Plural']):
            
            if preverb == 'e':
                preverb = 'ey' if region == 'PZ' else 'y'
            elif preverb != 'me':
                preverb = preverb[:-1]

        # Handle specific preverbs
        if preverb == 'me':
            root, prefix = self._handle_me_preverb(root, subject, region)
        elif preverb == 'do':
            root, prefix = self._handle_do_preverb(root, subject, region)
        elif preverb == 'ge':
            root, prefix = self._handle_ge_preverb(root, subject, region)
        elif preverb == 'go':
            root, prefix = self._handle_go_preverb(root, subject, region)

        return root, preverb, prefix

    def _handle_me_preverb(self, root: str, subject: str, region: str) -> Tuple[str, str]:
        """Handle 'me' preverb special cases."""
        first_letter = self.get_first_letter(root)
        
        if subject in ['S1_Singular', 'S1_Plural']:
            adjusted = self.adjust_prefix('v', first_letter, region)
            return root, f"me{adjusted}"
        elif subject in ['S2_Singular', 'S2_Plural']:
            adjusted = self.adjust_prefix('g', first_letter, region)
            return root, f"me{adjusted}"
        
        return root, 'me'

    def _handle_do_preverb(self, root: str, subject: str, region: str) -> Tuple[str, str]:
        """Handle 'do' preverb special cases."""
        if root.startswith(('diguraps', 'digurams')):
            root = root[1:]
            
        first_letter = self.get_first_letter(root)
        
        if subject in ['S3_Singular', 'S3_Plural']:
            prefix = 'd' if region == 'FA' else 'dv'
        elif subject in ['S1_Singular', 'S1_Plural']:
            adjusted = self.adjust_prefix('v', first_letter, region)
            prefix = f"do{adjusted}"
        elif subject in ['S2_Singular', 'S2_Plural']:
            adjusted = self.adjust_prefix('g', first_letter, region)
            prefix = f"do{adjusted}"
        else:
            prefix = 'do'
            
        return root, prefix

    def _handle_ge_preverb(self, root: str, subject: str, region: str) -> Tuple[str, str]:
        """Handle 'ge' preverb special cases."""
        first_letter = self.get_first_letter(root)
        
        if subject in ['S1_Singular', 'S1_Plural']:
            adjusted = self.adjust_prefix('v', first_letter, region)
            return root, f"ge{adjusted}"
        elif subject in ['S2_Singular', 'S2_Plural']:
            adjusted = self.adjust_prefix('g', first_letter, region)
            return root, f"ge{adjusted}"
        
        return root, 'gy'

    def _handle_go_preverb(self, root: str, subject: str, region: str) -> Tuple[str, str]:
        """Handle 'go' preverb special cases."""
        if subject in ['S3_Singular', 'S3_Plural']:
            prefix = 'g' if region == 'FA' else 'gv'
        else:
            prefix = f"go{subject_markers.get(subject, '')}"
            
        return root, prefix

    def process_suffix(self, root: str, suffix: str) -> str:
        """
        Process and attach suffix to root.
        
        Args:
            root: The verb root
            suffix: The suffix to attach
            
        Returns:
            Root with properly attached suffix
        """
        # Remove final 's' if present
        if root.endswith('s'):
            root = root[:-1]
            
        # Remove final 'en' if present
        if root.endswith('en'):
            root = root[:-2]
            
        # Special handling for roots ending in 'rs'
        if root.endswith('rs'):
            root = root[:-2]
            
        return root + suffix

    def split_compound_verb(self, verb: str) -> Tuple[str, str]:
        """
        Split a compound verb into its parts.
        
        Args:
            verb: The full verb form
            
        Returns:
            Tuple of (first_part, rest)
        """
        parts = verb.split()
        if len(parts) > 1:
            # Check if first part is a compound marker
            if parts[0] in self._compound_markers:
                return parts[0], ' '.join(parts[1:])
            return '', verb
        return '', verb

    def merge_compound_verb(self, first_part: str, rest: str) -> str:
        """
        Merge parts of a compound verb.
        
        Args:
            first_part: First part of the verb
            rest: Rest of the verb
            
        Returns:
            Complete verb form
        """
        if not first_part:
            return rest
        return f"{first_part} {rest}"