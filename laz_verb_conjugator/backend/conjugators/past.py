# lazuri/conjugators/past.py

from typing import Dict, Optional
from .base_conjugator import BaseVerbalConjugator

class IVDPastConjugator(BaseVerbalConjugator):
    """Past tense conjugator for IVD verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past tense suffixes for IVD verbs."""
        suffixes = {
            'S1_Singular': 'u',
            'S2_Singular': 'u',
            'S3_Singular': 'u',
            'S1_Plural': 'es',
            'S2_Plural': 'es',
            'S3_Plural': 'es'
        }
        if region == "AŞ" and subject == 'S3_Plural':
            suffixes['S3_Plural'] = 'ey'
        return suffixes[subject]

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past tense."""
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
        return root

class TVEPastConjugator(BaseVerbalConjugator):
    """Past tense conjugator for TVE verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past tense suffixes for TVE verbs."""
        suffixes = {
            'S1_Singular': 'i',
            'S2_Singular': 'i',
            'S3_Singular': 'u',
            'S1_Plural': 'it',
            'S2_Plural': 'it',
            'S3_Plural': 'es'
        }
        if region == "AŞ":
            suffixes['S3_Plural'] = 'ey'
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in past tense."""
        special_forms = {
            'ren': lambda r: 'ort̆',
            'oxenu': {
                'S1_Singular': lambda r: 'p̌qvi (p̌i)',
                'S1_Plural': lambda r: 'p̌qvit (p̌it)',
                'S2_Singular': lambda r: 'v' if r == "FA" else 'qv',
                'S2_Plural': lambda r: 'vit' if r == "FA" else 'qvit',
                'S3_Singular': lambda r: 'qvu',
                'S3_Plural': lambda r: 'qves'
            }
        }
        
        if infinitive in special_forms:
            if callable(special_forms[infinitive]):
                return special_forms[infinitive](region)
            elif subject in special_forms[infinitive]:
                return special_forms[infinitive][subject](region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past tense."""
        if root.endswith('rs'):
            root = root[:-1]
        elif root.endswith('ms'):
            root = root[:-1]
        return root

class TVMPastConjugator(BaseVerbalConjugator):
    """Past tense conjugator for TVM verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get past tense suffixes for TVM verbs."""
        suffixes = {
            'S1_Singular': 'i',
            'S2_Singular': 'i',
            'S3_Singular': 'u',
            'S1_Plural': 'it',
            'S2_Plural': 'it',
            'S3_Plural': 'es'
        }
        if region == "AŞ":
            suffixes['S3_Plural'] = 'ey'
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in past tense."""
        if infinitive in ('oxtimu', 'olva'):
            return 'id' + self._get_region_specific_suffix(subject, region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for past tense."""
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
        return root