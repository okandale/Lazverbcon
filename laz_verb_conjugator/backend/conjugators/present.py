# lazuri/conjugators/present.py

from typing import Dict, Optional
from .base_conjugator import BaseVerbalConjugator

class IVDPresentConjugator(BaseVerbalConjugator):
    """Present tense conjugator for IVD verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get present tense suffixes for IVD verbs."""
        suffixes = {
            'S1_Singular': '',
            'S2_Singular': '',
            'S3_Singular': '',
            'S1_Plural': 'an',
            'S2_Plural': 'an',
            'S3_Plural': 'an'
        }
        return suffixes[subject]

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for present tense."""
        # IVD verbs in present tense might need root modifications
        if root.endswith('rs'):
            return root[:-1]  # Remove final 's'
        return root

class TVEPresentConjugator(BaseVerbalConjugator):
    """Present tense conjugator for TVE verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get present tense suffixes for TVE verbs."""
        suffixes = {
            'S1_Singular': '',
            'S2_Singular': '',
            'S3_Singular': 's',
            'S1_Plural': 't',
            'S2_Plural': 't',
            'S3_Plural': 'an'
        }
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in present tense."""
        # Example of special case handling
        if infinitive == "ren":
            if region == "FA":
                if subject == "S1_Singular":
                    return "bore"
                if subject == "S1_Plural":
                    return "boret"
            elif region in ('PZ', 'AŞ'):
                if subject == "S3_Singular":
                    return "on"
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for present tense."""
        # Remove final 's' if present, unless it's S3_Singular
        if root.endswith('s') and subject != 'S3_Singular':
            return root[:-1]
        return root

class TVMPresentConjugator(BaseVerbalConjugator):
    """Present tense conjugator for TVM verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get present tense suffixes for TVM verbs."""
        suffixes = {
            'S1_Singular': 'r',
            'S2_Singular': 'r',
            'S3_Singular': 'n',
            'S1_Plural': 'rt',
            'S2_Plural': 'rt',
            'S3_Plural': 'nan'
        }
        return suffixes[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in present tense."""
        special_forms = {
            'ren': {
                'S1_Singular': lambda r: 'bore' if r == "FA" else '',
                'S2_Singular': lambda r: '(o)rer' if r == "AŞ" else '(o)re',
                'S3_Singular': lambda r: 'on' if r in ('PZ', 'AŞ') else "(o)ren",
                'S1_Plural': lambda r: 'boret' if r == "FA" else 'oret',
                'S2_Plural': lambda r: '(o)ret',
                'S3_Plural': lambda r: 'onan'
            }
        }
        
        if infinitive in special_forms and subject in special_forms[infinitive]:
            return special_forms[infinitive][subject](region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for present tense."""
        # Handle root modifications for present tense
        if root.endswith('en'):
            root = root[:-2]
        if root.endswith('s'):
            root = root[:-1]
        return root