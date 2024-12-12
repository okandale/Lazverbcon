# lazuri/handlers/ivd_handler.py

from typing import Dict, List, Optional, Tuple, Set
from ..core.base import ConjugationBase
from ..utils.phonetics import PhoneticProcessor
from ..core.data_manager import VerbDataManager

class IVDHandler(ConjugationBase):
    """
    Handler for Intransitive Verbs with Dative subjects (IVD).
    Implements specific conjugation rules and transformations for IVD verbs.
    """
    
    def __init__(self):
        super().__init__()
        self._phonetics = PhoneticProcessor()
        self._data_manager = VerbDataManager()
        self._initialize_rules()
        
    def _initialize_rules(self) -> None:
        """Initialize IVD-specific conjugation rules."""
        self.subject_markers = {
            'S1_Singular': 'm',
            'S2_Singular': 'g',
            'S3_Singular': '',
            'S1_Plural': 'm',
            'S2_Plural': 'g',
            'S3_Plural': ''
        }
        
        self.special_roots = {
            'diç̌irs': 'ç̌irs',
            'dvaç̌irs': 'ç̌irs',
            'oroms': {
                'O2': 'ǩ',
                'S1O3': 'p̌',
                'S1': 'p̌',
                'O1': 'mp̌'
            }
        }

    def process_root(self, infinitive: str, root: str, subject: str, 
                    obj: Optional[str] = None) -> str:
        """
        Process verb root according to IVD rules.
        
        Args:
            infinitive: Original infinitive form
            root: Verb root to process
            subject: Subject marker
            obj: Object marker (optional)
            
        Returns:
            Processed root
        """
        # Handle special roots
        if root in self.special_roots:
            if isinstance(self.special_roots[root], dict):
                if obj and obj.startswith('O2'):
                    return self.special_roots[root]['O2']
                elif subject.startswith('S1') and obj and obj.startswith('O3'):
                    return self.special_roots[root]['S1O3']
                elif subject.startswith('S1'):
                    return self.special_roots[root]['S1']
                elif obj and obj.startswith('O1'):
                    return self.special_roots[root]['O1']
            else:
                return self.special_roots[root]

        # Handle 'u' to 'i' conversion for certain subjects
        root = self._phonetics.handle_special_case_u(root, subject, '')
        
        # Remove 'en' ending if present
        if root.endswith('en'):
            root = root[:-2]
            
        # Remove final 's' if present
        if root.endswith('s'):
            root = root[:-1]
            
        return root

    def get_prefix(self, root: str, subject: str, obj: Optional[str], 
                  preverb: str, region: str) -> str:
        """
        Get appropriate prefix based on subject, object, and preverb.
        
        Args:
            root: Processed verb root
            subject: Subject marker
            obj: Object marker (optional)
            preverb: Preverb (if any)
            region: Dialect region
            
        Returns:
            Appropriate prefix
        """
        if preverb:
            return self._handle_preverb_prefix(root, subject, obj, preverb, region)
            
        prefix = self.subject_markers[subject]
        first_letter = self._phonetics.get_first_letter(root)
        
        # Handle object prefixes
        if obj:
            if obj.startswith('O2'):
                prefix = self._phonetics.adjust_prefix('g', first_letter, region)
            elif obj.startswith('O1'):
                prefix = 'm' + prefix
            elif subject.startswith('S1'):
                prefix = self._phonetics.adjust_prefix(prefix, first_letter, region)
                
        return prefix

    def _handle_preverb_prefix(self, root: str, subject: str, obj: Optional[str],
                             preverb: str, region: str) -> str:
        """Handle prefix formation with preverbs."""
        first_letter = self._phonetics.get_first_letter(root)
        
        if preverb in ('ge', 'e', 'ce'):
            if subject.startswith('S1'):
                return preverb + 'om'
            elif subject.startswith('S2'):
                return preverb + 'og'
            return preverb
            
        elif preverb == 'do':
            if subject.startswith('S3'):
                if obj and obj.startswith('O1'):
                    return f"do{'v' if region in ('PZ', 'AŞ', 'HO') else 'b'}"
                return 'd' if region == 'FA' else 'dv'
            elif subject.startswith('S1'):
                return 'do' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif subject.startswith('S2'):
                return 'do' + self._phonetics.adjust_prefix('g', first_letter, region)
            return 'do'
            
        return preverb

    def get_suffix(self, subject: str, obj: Optional[str], tense: str,
                  region: str) -> str:
        """Get appropriate suffix based on subject and tense."""
        # This will be implemented by specific tense conjugators
        raise NotImplementedError("Suffix handling is tense-specific")

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Main conjugation method for IVD verbs.
        
        Args:
            infinitive: Verb to conjugate
            subject: Subject marker
            obj: Object marker (optional)
            applicative: Whether to use applicative form
            causative: Whether to use causative form
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
                root = self.process_root(infinitive, forms, subject, obj)
                preverb = self._phonetics.get_preverb(infinitive)
                prefix = self.get_prefix(root, subject, obj, preverb, region)
                
                # The actual suffix will be added by the tense conjugator
                # Store the processed components for the conjugator
                results[region].append((
                    subject,
                    obj,
                    (prefix, root, preverb)  # Components for conjugator
                ))
                
        return results