from typing import Dict, List, Set, Optional
from pathlib import Path
import yaml
from .base_config import LazuriConfig

class VerbRules:
    """Configuration class for verb-specific rules and constraints."""
    
    def __init__(self):
        self.config = LazuriConfig()
        self._rules: Dict[str, Dict] = {}
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load default verb rules."""
        self._rules = {
            'preverbs': {
                'standard': ['ge', 'e', 'ce', 'do', 'ye'],
                'special': {
                    'go': {
                        'S1_Singular': 'gom',
                        'S2_Singular': 'gog',
                        'S3_Singular': 'go',
                        'S1_Plural': 'gom',
                        'S2_Plural': 'gog',
                        'S3_Plural': 'go'
                    },
                    'gy': {
                        'S1_Singular': 'gem',
                        'S2_Singular': 'geg',
                        'S3_Singular': 'gyo',
                        'S1_Plural': 'gem',
                        'S2_Plural': 'geg',
                        'S3_Plural': 'gyo'
                    }
                }
            },
            'phonetic_rules': {
                'FA': {
                    'v_rules': {
                        'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                        'b': ['l', 'a', 'e', 'i', 'o', 'u', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                        'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                        'm': ['n']
                    }
                },
                'default': {
                    'v_rules': {
                        'v': ['a', 'e', 'i', 'o', 'u'],
                        'p': ['t', 'k', 'ʒ', 'ç', 'f', 's', 'ş', 'x', 'h'],
                        'b': ['l', 'd', 'g', 'ž', 'c', 'v', 'z', 'j', 'ğ'],
                        'p̌': ['ç̌', 'ǩ', 'q', 'ǯ', 't̆'],
                        'm': ['n']
                    }
                }
            },
            'special_verbs': {
                'coxons': {'no_object': True},
                'cozun': {'no_object': True},
                'gyožin': {'no_object': True}
            },
            'verb_categories': {
                'IVD': {
                    'can_take_object': True,
                    'supported_tenses': ['present', 'past', 'future', 'past_progressive']
                },
                'TVE': {
                    'can_take_object': True,
                    'supported_tenses': ['present', 'past', 'future', 'past_progressive'],
                    'supported_aspects': ['potential', 'passive']
                },
                'TVM': {
                    'can_take_object': False,
                    'supported_tenses': ['present', 'past', 'future', 'past_progressive'],
                    'supported_aspects': ['potential', 'passive']
                }
            },
            'subject_object_rules': {
                'invalid_combinations': [
                    ('S1_Singular', 'O1_Singular'),
                    ('S1_Plural', 'O1_Plural'),
                    ('S2_Singular', 'O2_Singular'),
                    ('S2_Plural', 'O2_Plural')
                ]
            }
        }

    def load_rules(self, rules_file: Path) -> None:
        """
        Load rules from a YAML file.
        
        Args:
            rules_file: Path to the rules file
            
        Raises:
            FileNotFoundError: If rules file doesn't exist
            yaml.YAMLError: If rules file is invalid
        """
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_file}")
            
        with rules_file.open('r', encoding='utf-8') as f:
            loaded_rules = yaml.safe_load(f)
            
        # Deep update current rules
        self._deep_update(self._rules, loaded_rules)

    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> None:
        """Recursively update a dictionary."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def get_preverb_rule(self, preverb: str, subject: Optional[str] = None) -> Optional[str]:
        """Get preverb rule for a given subject."""
        if preverb in self._rules['preverbs']['special']:
            if subject:
                return self._rules['preverbs']['special'][preverb].get(subject, preverb)
            return preverb
        return preverb if preverb in self._rules['preverbs']['standard'] else None

    def get_phonetic_rules(self, region: str) -> Dict:
        """Get phonetic rules for a region."""
        return self._rules['phonetic_rules'].get(region, 
               self._rules['phonetic_rules']['default'])

    def get_verb_restrictions(self, verb: str) -> Dict:
        """Get any special restrictions for a verb."""
        return self._rules['special_verbs'].get(verb, {})

    def get_category_rules(self, category: str) -> Dict:
        """Get rules for a verb category."""
        return self._rules['verb_categories'].get(category, {})

    def is_valid_combination(self, subject: str, obj: str) -> bool:
        """Check if a subject-object combination is valid."""
        return (subject, obj) not in self._rules['subject_object_rules']['invalid_combinations']

    def add_special_verb(self, verb: str, restrictions: Dict) -> None:
        """Add special restrictions for a verb."""
        self._rules['special_verbs'][verb] = restrictions

    @property
    def all_rules(self) -> Dict:
        """Get complete rules dictionary."""
        return self._rules.copy()