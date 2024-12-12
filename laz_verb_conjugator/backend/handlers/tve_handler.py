# lazuri/handlers/tve_handler.py

from typing import Dict, List, Optional, Tuple, Set
from ..core.base import ConjugationBase
from ..utils.phonetics import PhoneticProcessor
from ..core.data_manager import VerbDataManager

class TVEHandler(ConjugationBase):
    """
    Handler for Transitive Verbs with Ergative subjects (TVE).
    Implements specific conjugation rules and transformations for TVE verbs.
    """
    
    def __init__(self):
        super().__init__()
        self._phonetics = PhoneticProcessor()
        self._data_manager = VerbDataManager()
        self._initialize_rules()
        
    def _initialize_rules(self) -> None:
        """Initialize TVE-specific conjugation rules."""
        self.subject_markers = {
            'S1_Singular': 'v',
            'S2_Singular': '',
            'S3_Singular': '',
            'S1_Plural': 'v',
            'S2_Plural': '',
            'S3_Plural': ''
        }
        
        self.special_roots = {
            'oç̌ǩomu': {
                'causative': 'çams',
                'applicative': 'ç̌ǩomums'
            },
            'oşǩomu': {
                'causative': 'çams',
                'applicative': 'şǩomums'
            },
            'oxenu': {
                'applicative': 'xenums',
                'causative': 'xenums'
            },
            'oxvenu': {
                'applicative': 'xvenums',
                'causative': 'xvenums'
            }
        }
        
        self.ardeşen_rules = {
            'y_ending': {
                'S3_Singular': lambda root: root,
                'default': lambda root: root[:-1] + 'm'
            }
        }

    def process_root(self, infinitive: str, root: str, subject: str,
                    obj: Optional[str] = None, applicative: bool = False,
                    causative: bool = False) -> str:
        """
        Process verb root according to TVE rules.
        
        Args:
            infinitive: Original infinitive form
            root: Verb root to process
            subject: Subject marker
            obj: Object marker (optional)
            applicative: Whether to use applicative form
            causative: Whether to use causative form
            
        Returns:
            Processed root
        """
        # Handle special roots
        if infinitive in self.special_roots:
            if causative:
                return self.special_roots[infinitive]['causative']
            elif applicative:
                return self.special_roots[infinitive]['applicative']
        
        # Handle Ardeşen rule (verbs ending in 'y')
        if root.endswith('y'):
            rule = self.ardeşen_rules['y_ending']
            if subject == 'S3_Singular':
                return rule['S3_Singular'](root)
            return rule['default'](root)
        
        # Handle applicative and causative markers
        if applicative and causative:
            if infinitive in ('oşu', 'dodvu', 'otku'):
                root = root[:-3] + 'vapap'
            elif root.endswith(('ms', 'ps')):
                root = root[:-3] + 'ap'
            elif root.endswith(('umers', 'amers')):
                root = root[:-5] + 'ap'
            elif root.endswith('rs'):
                root = root[:-1] + 'ap'
            elif root.endswith('y'):
                root = root[:-2] + 'ap'
        elif applicative:
            if root in ('işums', 'işups', 'idums', 'itkums', 'itkups'):
                root = root[:-3] + 'v'
            elif root.endswith(('ms', 'ps')):
                root = root[:-3]
            elif root.endswith('um'):
                root = root[:-2] + 'ams'
            elif root.endswith('y'):
                root = root[:-2]
        elif causative:
            if root == 'digurams':
                return root
            elif root in ('oşums', 'oşups', 'odums', 'otkums', 'otkups'):
                root = root[:-3] + 'vap'
            elif root.endswith(('ms', 'ps')):
                root = root[:-3] + 'ap'
            elif root.endswith(('umers', 'amers')):
                root = root[:-5] + 'ap'
            elif root.endswith('rs'):
                root = root[:-1] + 'ap'
            elif root.endswith('y'):
                root = root[:-2] + 'ap'
            
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
        
        # Special case for 'oroms'
        if root == 'oroms':
            if obj and obj.startswith('O2'):
                return 'ǩ'
            elif subject.startswith('S1') and obj and obj.startswith('O3'):
                return 'p̌'
            elif subject.startswith('S1'):
                return 'p̌'
            elif obj and obj.startswith('O1'):
                return 'mp̌'
            return prefix
        
        # Handle object prefixes
        if obj:
            if obj.startswith('O2'):
                prefix = self._phonetics.adjust_prefix('g', first_letter, region)
            elif obj.startswith('O1'):
                prefix = 'm' + prefix
            elif subject.startswith('S3') and obj.startswith('O1'):
                prefix = 'v' if region in ('PZ', 'AŞ', 'HO') else 'b'
                if infinitive in ('olimbu', 'oropumu'):
                    prefix = '(go)' + prefix
                
        return prefix

    def _handle_preverb_prefix(self, root: str, subject: str, obj: Optional[str],
                             preverb: str, region: str) -> str:
        """Handle prefix formation with preverbs."""
        first_letter = self._phonetics.get_first_letter(root)
        
        if preverb == 'oxo':
            if obj and obj.startswith('O2'):
                return 'oxo' + self._phonetics.adjust_prefix('g', first_letter, region)
            elif subject.startswith('S1'):
                return 'oxo' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif obj and obj.startswith('O1'):
                return 'oxom'
            return 'oxo'
            
        elif preverb == 'oǩo':
            if obj and obj.startswith('O2'):
                return 'oǩo' + self._phonetics.adjust_prefix('g', first_letter, region)
            elif subject.startswith('S1'):
                return 'oǩo' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif obj and obj.startswith('O1'):
                return 'oǩom'
            return 'oǩo'
            
        elif preverb == 'go':
            if subject.startswith('S3'):
                if obj and obj.startswith('O1'):
                    return f"go{'v' if region in ('PZ', 'AŞ', 'HO') else 'b'}"
                return 'g' if region == 'FA' else 'gv'
            elif subject.startswith('S1'):
                return 'go' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif subject.startswith('S2'):
                return 'go' + self._phonetics.adjust_prefix('g', first_letter, region)
            return 'go'
            
        elif preverb == 'dolo':
            if subject.startswith('S1'):
                return 'dolo' + self._phonetics.adjust_prefix('v', first_letter, region)
            elif subject.startswith('S2'):
                return 'dolo' + self._phonetics.adjust_prefix('g', first_letter, region)
            elif obj and obj.startswith('O1'):
                return 'dolom'
            return 'dolo'
            
        return preverb

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Main conjugation method for TVE verbs.
        
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
                root = self.process_root(infinitive, forms, subject, obj, 
                                      applicative, causative)
                preverb = self._phonetics.get_preverb(infinitive)
                
                # Handle optional preverb
                if use_optional_preverb and not preverb:
                    if subject in ['O3_Singular', 'O3_Plural']:
                        prefix = 'k'
                    else:
                        prefix = 'ko' + self.get_prefix(root, subject, obj, '', region)
                else:
                    prefix = self.get_prefix(root, subject, obj, preverb, region)
                
                # The actual suffix will be added by the tense conjugator
                results[region].append((
                    subject,
                    obj,
                    (prefix, root, preverb)  # Components for conjugator
                ))
                
        return results