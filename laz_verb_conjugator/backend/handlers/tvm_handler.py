# lazuri/handlers/tvm_handler.py

from typing import Dict, List, Optional, Tuple, Set
from ..core.base import ConjugationBase
from ..utils.phonetics import PhoneticProcessor
from ..core.data_manager import VerbDataManager

class TVMHandler(ConjugationBase):
    """
    Handler for Transitive Verbs with Middle voice (TVM).
    Implements specific conjugation rules and transformations for TVM verbs.
    """
    
    def __init__(self):
        super().__init__()
        self._phonetics = PhoneticProcessor()
        self._data_manager = VerbDataManager()
        self._initialize_rules()
        
    def _initialize_rules(self) -> None:
        """Initialize TVM-specific conjugation rules."""
        self.subject_markers = {
            'S1_Singular': 'v',
            'S2_Singular': '',
            'S3_Singular': '',
            'S1_Plural': 'v',
            'S2_Plural': '',
            'S3_Plural': ''
        }
        
        self.special_roots = {
            'ren': {
                'present': {
                    'S1_Singular': lambda region: 'ore' if region == "FA" else '',
                    'S2_Singular': lambda region: '(o)rer' if region == "AŞ" else '(o)re',
                    'S3_Singular': lambda region: 'on' if region in ('PZ', 'AŞ') else "(o)ren",
                    'S1_Plural': lambda region: 'ore',
                    'S2_Plural': lambda region: '(o)re',
                    'S3_Plural': lambda region: 'on' if region == 'AŞ' else "(o)ren"
                },
                'past': lambda region, subject: 'ort̆'
            }
        }
        
        self.pre_suffixes = {
            'potential': {
                'S1_Singular': 'en',
                'S2_Singular': 'en',
                'S3_Singular': 'en',
                'S1_Plural': 'enan',
                'S2_Plural': 'enan',
                'S3_Plural': 'enan'
            },
            'passive': {
                'S1_Singular': 'er',
                'S2_Singular': 'er',
                'S3_Singular': 'en',
                'S1_Plural': 'ert',
                'S2_Plural': 'ert',
                'S3_Plural': 'enan'
            }
        }

    def process_root(self, infinitive: str, root: str, subject: str,
                    tense: str = 'present') -> str:
        """
        Process verb root according to TVM rules.
        
        Args:
            infinitive: Original infinitive form
            root: Verb root to process
            subject: Subject marker
            tense: Verb tense
            
        Returns:
            Processed root
        """
        # Handle special verbs
        if infinitive in self.special_roots:
            if tense in self.special_roots[infinitive]:
                if callable(self.special_roots[infinitive][tense]):
                    return self.special_roots[infinitive][tense](subject)
                else:
                    return self.special_roots[infinitive][tense][subject]
        
        # Standard root processing
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
            
        return root

    def get_prefix(self, root: str, subject: str, preverb: str, region: str) -> str:
        """
        Get appropriate prefix based on subject and preverb.
        
        Args:
            root: Processed verb root
            subject: Subject marker
            preverb: Preverb (if any)
            region: Dialect region
            
        Returns:
            Appropriate prefix
        """
        if preverb:
            return self._handle_preverb_prefix(root, subject, preverb, region)
            
        prefix = self.subject_markers[subject]
        first_letter = self._phonetics.get_first_letter(root)
        
        # Standard prefix adjustments
        if subject.startswith('S1'):
            return self._phonetics.adjust_prefix(prefix, first_letter, region)
            
        return prefix

    def _handle_preverb_prefix(self, root: str, subject: str, preverb: str,
                             region: str) -> str:
        """Handle prefix formation with preverbs."""
        first_letter = self._phonetics.get_first_letter(root)
        
        if preverb == 'e':
            if subject.startswith('S3'):
                return 'y' if region != 'PZ' else 'ey'
            elif subject.startswith('S1'):
                return 'e' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif subject.startswith('S2'):
                return 'e' + self._phonetics.adjust_prefix('g', first_letter, region)
            
        elif preverb == 'me':
            if subject.startswith('S1'):
                return 'me' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif subject.startswith('S2'):
                return 'me' + self._phonetics.adjust_prefix('g', first_letter, region)
            return 'n' if first_letter in 'aeiou' else 'me'
            
        return preverb

    def get_special_suffix(self, subject: str, aspect: Optional[str] = None) -> Optional[str]:
        """Get special suffix for aspects like potential or passive."""
        if not aspect:
            return None
            
        if aspect in self.pre_suffixes:
            return self.pre_suffixes[aspect].get(subject)
            
        return None

    def conjugate(self, infinitive: str, subject: str, tense: str = 'present',
                 aspect: Optional[str] = None, use_optional_preverb: bool = False
                 ) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Main conjugation method for TVM verbs.
        
        Args:
            infinitive: Verb to conjugate
            subject: Subject marker
            tense: Verb tense
            aspect: Verb aspect (optional)
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to conjugation tuples
        """
        verb_data = self._data_manager.get_verb_data(infinitive)
        if not verb_data:
            raise ValueError(f"Verb not found: {infinitive}")
            
        results: Dict[str, List[Tuple[str, str, str]]] = {}
        
        for forms, region_str in verb_data[0]:
            regions = [r.strip() for r in region_str.split(',')]
            
            for region in regions:
                if region not in results:
                    results[region] = []
                    
                # Process the verb parts
                root = self.process_root(infinitive, forms, subject, tense)
                preverb = self._phonetics.get_preverb(infinitive)
                
                # Handle optional preverb
                if use_optional_preverb and not preverb:
                    prefix = 'ko' + self.get_prefix(root, subject, '', region)
                else:
                    prefix = self.get_prefix(root, subject, preverb, region)
                
                # Get aspect-specific suffix if needed
                special_suffix = self.get_special_suffix(subject, aspect)
                
                # The actual tense suffix will be added by the conjugator
                results[region].append((
                    subject,
                    None,  # TVM verbs don't take objects
                    (prefix, root, preverb, special_suffix)  # Components for conjugator
                ))
                
        return results