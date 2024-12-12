# lazuri/conjugators/past_progressive.py

from typing import Dict, Optional
from .base_conjugator import BaseVerbalConjugator

class IVDPastProgressiveConjugator(BaseVerbalConjugator):
    """Past progressive tense conjugator for IVD verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past progressive tense suffixes for IVD verbs."""
        root_ends_with_r = bool(getattr(self, '_current_root_ends_with_r', False))
        suffixes = {
            'S1_Singular': 't̆u' if root_ends_with_r else 'rt̆u',
            'S2_Singular': 't̆u' if root_ends_with_r else 'rt̆u',
            'S3_Singular': 't̆u' if root_ends_with_r else 'rt̆u',
            'S1_Plural': 't̆es' if root_ends_with_r else 'rt̆es',
            'S2_Plural': 't̆es' if root_ends_with_r else 'rt̆es',
            'S3_Plural': 't̆es' if root_ends_with_r else 'rt̆es'
        }
        return suffixes[subject]

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past progressive tense."""
        # Store whether root ends with 'r' for suffix determination
        self._current_root_ends_with_r = root.endswith('r')
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-1]
        return root

class TVEPastProgressiveConjugator(BaseVerbalConjugator):
    """Past progressive tense conjugator for TVE verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past progressive tense suffixes for TVE verbs."""
        suffixes = {
            'S1_Singular': 'ert̆i',
            'S2_Singular': 'ert̆i',
            'S3_Singular': 'ert̆u',
            'S1_Plural': 'ert̆it',
            'S2_Plural': 'ert̆it',
            'S3_Plural': 'ert̆es'
        }
        if region == "AŞ":
            suffixes['S3_Plural'] = 'ert̆ey'
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in past progressive tense."""
        special_verbs = {
            'oxenu': {
                'S1_Singular': lambda r: 'p̌qvi',
                'S2_Singular': lambda r: '' if r in ('AŞ', 'PZ') else 'v',
                'S3_Singular': lambda r: 'qv' if r == "HO" else '' if r in ('AŞ', 'PZ') else 'v',
                'S1_Plural': lambda r: 'p̌qvit',
                'S2_Plural': lambda r: 'vit' if r == "FA" else 'qvit',
                'S3_Plural': lambda r: 'qves'
            }
        }
        
        if infinitive in special_verbs and subject in special_verbs[infinitive]:
            return special_verbs[infinitive][subject](region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past progressive tense."""
        if root.endswith('rs'):
            root = root[:-1]
        if root.endswith('ms'):
            root = root[:-1]
        return root

class TVMPastProgressiveConjugator(BaseVerbalConjugator):
    """Past progressive tense conjugator for TVM verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past progressive tense suffixes for TVM verbs."""
        suffixes = {
            'S1_Singular': 'rt̆i',
            'S2_Singular': 'rt̆i',
            'S3_Singular': 'rt̆u',
            'S1_Plural': 'rt̆it',
            'S2_Plural': 'rt̆it',
            'S3_Plural': 'rt̆es'
        }
        if region == "AŞ":
            suffixes['S3_Plural'] = 'rt̆ey'
            
        # Handle causative forms if present
        if getattr(self, '_is_causative', False):
            suffixes = {
                'S1_Singular': 'apinert̆i',
                'S2_Singular': 'apinert̆i',
                'S3_Singular': 'apinert̆u',
                'S1_Plural': 'apinert̆it',
                'S2_Plural': 'apinert̆it',
                'S3_Plural': 'apinent̆es'
            }
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in past progressive tense."""
        special_verbs = {
            'oxtimu': lambda subj, reg: 'id' + self._get_region_specific_suffix(subj, reg),
            'olva': lambda subj, reg: 'id' + self._get_region_specific_suffix(subj, reg)
        }
        
        if infinitive in special_verbs:
            return special_verbs[infinitive](subject, region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past progressive tense."""
        # Remove common endings
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
            
        # Handle Ardeşen rule
        if root.endswith('y'):
            if subject == 'S3_Singular':
                return root
            return root[:-1] + 'm'
            
        return root
        
    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """Override to handle causative flag."""
        self._is_causative = causative
        return super().conjugate(infinitive, subject, obj, applicative, causative, use_optional_preverb)