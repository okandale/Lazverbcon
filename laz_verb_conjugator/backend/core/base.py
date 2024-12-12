# lazuri/core/base.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Set

class ConjugationBase(ABC):
    """
    Base class for all conjugation operations.
    Provides common functionality and defines required interface.
    """
    
    def __init__(self):
        self.preverbs_rules = {
            ('ge', 'e', 'ce', 'do', 'ye'): {
                'S1_Singular': 'om',
                'S2_Singular': 'og',
                'S3_Singular': '',
                'S1_Plural': 'om',
                'S2_Plural': 'og',
                'S3_Plural': ''
            },
            ('go',): {
                'S1_Singular': 'gom',
                'S2_Singular': 'gog',
                'S3_Singular': 'go',
                'S1_Plural': 'gom',
                'S2_Plural': 'gog',
                'S3_Plural': 'go'
            },
            ('gy',): {
                'S1_Singular': 'gem',
                'S2_Singular': 'geg',
                'S3_Singular': 'gyo',
                'S1_Plural': 'gem',
                'S2_Plural': 'geg',
                'S3_Plural': 'gyo'
            },
            ('coz',): {
                'S1_Singular': 'cem',
                'S2_Singular': 'ceg',
                'S3_Singular': 'coz',
                'S1_Plural': 'cem',
                'S2_Plural': 'ceg',
                'S3_Plural': 'coz'
            }
        }

        self.phonetic_rules_map = {
            'FA': {
                'v': {
                    'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                    'b': ['l', 'a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                    'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                    'm': ['n']
                }
            },
            'default': {
                'v': {
                    'v': ['a', 'e', 'i', 'o', 'u'],
                    'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                    'b': ['l', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                    'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                    'm': ['n']
                }
            }
        }

    def get_personal_pronouns(self, region: str) -> Dict[str, str]:
        """Get personal pronouns for a given region."""
        return {
            'S1_Singular': 'ma',
            'S2_Singular': 'si',
            'S3_Singular': 'heyas' if region == "FA" else 'himus' if region == 'PZ' else 'him' if region == 'AŞ' else '(h)emus',
            'O3_Singular': 'heya' if region == "FA" else 'him' if region in ('AŞ', 'PZ') else '(h)em',
            'S1_Plural': 'çku' if region == "FA" else 'şǩu' if region in ('AŞ', 'PZ') else 'çki',
            'S2_Plural': 'tkva' if region == "FA" else 't̆ǩva' if region in ('AŞ', 'PZ') else 'tkvan',
            'S3_Plural': 'hentepes' if region == "FA" else 'hinis' if region == 'PZ' else 'hini' if region == 'AŞ' else 'entepes',
            'O3_Plural': 'hentepe',
            'O1_Singular': 'ma',
            'O2_Singular': 'si',
            'O1_Plural': 'çku',
            'O2_Plural': 'tkva'
        }

    @staticmethod
    def process_compound_verb(verb: str) -> str:
        """Extract the main part of a compound verb."""
        return ' '.join(verb.split()[1:]) if len(verb.split()) > 1 else verb

    @staticmethod
    def get_first_word(verb: str) -> str:
        """Get the first word of a compound verb."""
        return verb.split()[0] if len(verb.split()) > 1 else ''

    @staticmethod
    def get_first_letter(root: str) -> str:
        """Get the first letter considering special characters."""
        if len(root) > 1 and root[:2] in ['t̆', 'ç̌', 'ǩ', 'p̌']:
            return root[:2]
        return root[0]

    @staticmethod
    def get_first_vowel_index(word: str) -> int:
        """Find the index of the first vowel in a word."""
        vowels = "aeiou"
        for index, char in enumerate(word):
            if char in vowels:
                return index
        return -1

    def handle_special_case_u(self, root: str, subject: str, preverb: str) -> str:
        """Handle special cases for verbs starting with 'u' and verbs with 'i'."""
        if root.startswith('u'):
            if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                root = 'i' + root[1:]

        if preverb == 'd':
            first_vowel_index = self.get_first_vowel_index(root)
            if first_vowel_index != -1 and root[first_vowel_index] == 'i':
                if subject in ['S1_Singular', 'S2_Singular', 'S1_Plural', 'S2_Plural']:
                    root = root[:first_vowel_index] + 'a' + root[first_vowel_index + 1:]

        return root

    def get_preverb_form(self, preverb: str, subject: str) -> str:
        """Get the correct preverb form for a given subject."""
        for preverb_group, rules in self.preverbs_rules.items():
            if preverb in preverb_group:
                return rules.get(subject, preverb)
        return preverb

    def adjust_prefix_for_phonetics(self, prefix: str, first_letter: str, region: str) -> str:
        """
        Adjust prefix based on phonetic rules for a specific region.
        
        Args:
            prefix: The initial prefix
            first_letter: The first letter of the root
            region: The dialect region
            
        Returns:
            Adjusted prefix according to phonetic rules
        """
        phonetic_rules = self.phonetic_rules_map.get(region, self.phonetic_rules_map['default'])
        rules = phonetic_rules['v']
        
        for target, letters in rules.items():
            if first_letter in letters:
                return target
        return prefix

    def handle_preverb(self, preverb: str, root: str, subject: str, obj: Optional[str],
                      region: str) -> Tuple[str, str, str]:
        """
        Handle preverb modifications and return modified components.
        
        Args:
            preverb: The preverb to process
            root: The verb root
            subject: The subject marker
            obj: The object marker (if any)
            region: The dialect region
            
        Returns:
            Tuple of (modified_preverb, modified_root, prefix)
        """
        if not preverb:
            return '', root, ''

        first_letter = self.get_first_letter(root)
        prefix = ''

        if preverb in ('ge', 'e', 'ce'):
            if subject.startswith('S1'):
                prefix = f"{preverb}om"
            elif subject.startswith('S2'):
                prefix = f"{preverb}og"
            else:
                prefix = preverb
        elif preverb in ('do', 'go'):
            # Special handling for do/go preverbs
            if subject.startswith('S3') and not obj:
                return '', root, ''
            
            root = root[2:] if region in ('PZ', 'AŞ', 'HO') else root[1:]
            if subject.startswith('S3'):
                if obj and obj.startswith('O1'):
                    adjusted = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                    prefix = f"{preverb}{adjusted}"
                else:
                    prefix = preverb[0] if region == 'FA' else f"{preverb[0]}v"
            else:
                prefix = f"{preverb}{self.get_subject_marker(subject)}"

        return preverb, root, prefix

    def get_subject_marker(self, subject: str) -> str:
        """Get the basic subject marker."""
        markers = {
            'S1': 'm',
            'S2': 'g',
            'S3': ''
        }
        return markers.get(subject[:2], '')

    def validate_combination(self, subject: str, obj: Optional[str]) -> bool:
        """
        Validate subject-object combination.
        
        Args:
            subject: The subject marker
            obj: The object marker (if any)
            
        Returns:
            Boolean indicating if combination is valid
        """
        if not obj:
            return True
            
        invalid_combinations = [
            ('S1', 'O1'),
            ('S2', 'O2')
        ]
        
        subject_prefix = subject[:2]
        object_prefix = obj[:2]
        
        return (subject_prefix, object_prefix) not in invalid_combinations

    @abstractmethod
    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Abstract method for conjugation implementation in derived classes.
        
        Args:
            infinitive: The infinitive form of the verb
            subject: The subject marker
            obj: The object marker (optional)
            applicative: Whether to apply applicative form
            causative: Whether to apply causative form
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to lists of conjugation tuples
        """
        raise NotImplementedError("Conjugate method must be implemented by derived classes")

    @abstractmethod
    def get_suffixes(self, region: str) -> Dict[str, str]:
        """
        Abstract method to get tense-specific suffixes.
        
        Args:
            region: The dialect region
            
        Returns:
            Dictionary mapping subject types to suffixes
        """
        raise NotImplementedError("Get_suffixes method must be implemented by derived classes")