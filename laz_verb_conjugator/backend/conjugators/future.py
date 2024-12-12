# lazuri/conjugators/future.py

from typing import Dict, Optional
from .base_conjugator import BaseVerbalConjugator

class IVDFutureConjugator(BaseVerbalConjugator):
    """Future tense conjugator for IVD verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get future tense suffixes for IVD verbs."""
        suffixes = {
            'HO': {
                'S1_Singular': 'aminon',
                'S2_Singular': 'aginon',
                'S3_Singular': 'asinon',
                'S1_Plural': 'aminonan',
                'S2_Plural': 'aginonan',
                'S3_Plural': 'asinonan'
            },
            'PZ': {
                'S1_Singular': 'are',
                'S2_Singular': 'are',
                'S3_Singular': 'asere',
                'S1_Plural': 'atere',
                'S2_Plural': 'atere',
                'S3_Plural': 'anere'
            },
            'default': {
                'S1_Singular': 'are',
                'S2_Singular': 'are',
                'S3_Singular': 'asen',
                'S1_Plural': 'aten',
                'S2_Plural': 'aten',
                'S3_Plural': 'anen'
            }
        }
        return suffixes.get(region, suffixes['default'])[subject]

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for future tense."""
        if root.endswith('rs'):
            return root[:-1]
        if root.endswith('en'):
            root = root[:-1]
        return root

class TVEFutureConjugator(BaseVerbalConjugator):
    """Future tense conjugator for TVE verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get future tense suffixes for TVE verbs."""
        suffixes = {
            'HO': {
                'S1_Singular': 'aminon',
                'S2_Singular': 'aginon',
                'S3_Singular': 'asinon',
                'S1_Plural': 'aminonan',
                'S2_Plural': 'aginonan',
                'S3_Plural': 'asinonan'
            },
            'PZ': {
                'S1_Singular': 'are',
                'S2_Singular': 'are',
                'S3_Singular': 'asere',
                'S1_Plural': 'atere',
                'S2_Plural': 'atere',
                'S3_Plural': 'anere'
            },
            'default': {
                'S1_Singular': 'are',
                'S2_Singular': 'are',
                'S3_Singular': 'asen',
                'S1_Plural': 'aten',
                'S2_Plural': 'aten',
                'S3_Plural': 'anen'
            }
        }
        return suffixes.get(region, suffixes['default'])[subject]

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle special cases in future tense."""
        special_roots = {
            'oxenu': {
                'S1_Singular': lambda r: 'p̌',
                'S2_Singular': lambda r: '' if r in ('AŞ', 'PZ') else 'v',
                'S3_Singular': lambda r: 'q' if r == "HO" else '' if r in ('AŞ', 'PZ') else 'v',
                'S3_Plural': lambda r: 'qvan' if r == "HO" else ''
            }
        }

        if infinitive in special_roots and subject in special_roots[infinitive]:
            special_root = special_roots[infinitive][subject](region)
            if special_root:
                return special_root + self._get_region_specific_suffix(subject, region)
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for future tense."""
        if root.endswith('rs'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
        return root

class TVMFutureConjugator(BaseVerbalConjugator):
    """Future tense conjugator for TVM verbs."""
    
    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get future tense suffixes for TVM verbs."""
        suffixes = {
            'HO': {
                'S1_Singular': 'aminon',
                'S2_Singular': 'aginon',
                'S3_Singular': 'asinon',
                'S1_Plural': 'aminonan',
                'S2_Plural': 'aginonan',
                'S3_Plural': 'asunonan'
            },
            'PZ': {
                'S1_Singular': 'asere',
                'S2_Singular': 'asere',
                'S3_Singular': 'asere',
                'S1_Plural': 'anere',
                'S2_Plural': 'anere',
                'S3_Plural': 'anere'
            },
            'default': {
                'S1_Singular': 'asen',
                'S2_Singular': 'asen',
                'S3_Singular': 'asen',
                'S1_Plural': 'anen',
                'S2_Plural': 'anen',
                'S3_Plural': 'anen'
            }
        }
        return suffixes.get(region, suffixes['default'])[subject]

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root for future tense."""
        if root.endswith('s'):
            root = root[:-1]
        if root.endswith('en'):
            root = root[:-2]
        return root