# lazuri/core/validator.py

from typing import Optional, Set, Dict, List
from .data_manager import VerbDataManager

class ConjugationValidator:
    """
    Handles validation of conjugation inputs and combinations.
    Provides error checking and validation for all conjugation operations.
    """

    def __init__(self):
        self._data_manager = VerbDataManager()
        self._valid_tenses = {'present', 'past', 'future', 'past_progressive'}
        self._valid_aspects = {'potential', 'passive'}
        self._valid_subjects = {
            'S1_Singular', 'S2_Singular', 'S3_Singular',
            'S1_Plural', 'S2_Plural', 'S3_Plural'
        }
        self._valid_objects = {
            'O1_Singular', 'O2_Singular', 'O3_Singular',
            'O1_Plural', 'O2_Plural', 'O3_Plural'
        }
        self._invalid_combinations = {
            ('S1_Singular', 'O1_Singular'), ('S1_Plural', 'O1_Plural'),
            ('S2_Singular', 'O2_Singular'), ('S2_Plural', 'O2_Plural')
        }
        self._special_restrictions = {
            'coxons': {'no_object': True},
            'cozun': {'no_object': True},
            'gyožin': {'no_object': True}
        }

    def validate_verb(self, infinitive: str) -> bool:
        """
        Validate that a verb exists in the database.
        
        Args:
            infinitive: The infinitive form to validate
            
        Returns:
            Boolean indicating if verb is valid
        """
        return self._data_manager.verify_verb_exists(infinitive.lower())

    def validate_tense(self, tense: str) -> bool:
        """
        Validate that a tense is supported.
        
        Args:
            tense: The tense to validate
            
        Returns:
            Boolean indicating if tense is valid
        """
        return tense in self._valid_tenses

    def validate_aspect(self, aspect: str) -> bool:
        """
        Validate that an aspect is supported.
        
        Args:
            aspect: The aspect to validate
            
        Returns:
            Boolean indicating if aspect is valid
        """
        return aspect in self._valid_aspects

    def validate_subject(self, subject: str) -> bool:
        """
        Validate that a subject marker is valid.
        
        Args:
            subject: The subject marker to validate
            
        Returns:
            Boolean indicating if subject is valid
        """
        return subject in self._valid_subjects

    def validate_object(self, obj: Optional[str]) -> bool:
        """
        Validate that an object marker is valid if provided.
        
        Args:
            obj: The object marker to validate
            
        Returns:
            Boolean indicating if object is valid
        """
        return obj is None or obj in self._valid_objects

    def validate_combination(self, subject: str, obj: Optional[str]) -> bool:
        """
        Validate that a subject-object combination is valid.
        
        Args:
            subject: The subject marker
            obj: The object marker
            
        Returns:
            Boolean indicating if combination is valid
        """
        if obj is None:
            return True
        return (subject, obj) not in self._invalid_combinations

    def validate_verb_object_compatibility(self, infinitive: str, obj: Optional[str]) -> bool:
        """
        Validate that a verb can take an object (if provided).
        
        Args:
            infinitive: The infinitive form
            obj: The object marker
            
        Returns:
            Boolean indicating if verb-object combination is valid
        """
        if obj is None:
            return True

        verb_type = self._data_manager.get_verb_type(infinitive.lower())
        if not verb_type:
            return False

        # Check special restrictions
        if infinitive in self._special_restrictions:
            restrictions = self._special_restrictions[infinitive]
            if restrictions.get('no_object', False) and obj is not None:
                return False

        # TVM verbs can't take objects
        if verb_type == 'TVM' and obj is not None:
            return False

        return True

    def validate_aspect_compatibility(self, infinitive: str, aspect: str) -> bool:
        """
        Validate that a verb supports a specific aspect.
        
        Args:
            infinitive: The infinitive form
            aspect: The aspect to validate
            
        Returns:
            Boolean indicating if aspect is compatible
        """
        verb_type = self._data_manager.get_verb_type(infinitive.lower())
        if not verb_type:
            return False

        aspect_support = {
            'potential': ['TVE', 'TVM'],
            'passive': ['TVE', 'TVM']
        }

        return verb_type in aspect_support.get(aspect, [])

    def validate_region(self, region: str) -> bool:
        """
        Validate that a region exists in the database.
        
        Args:
            region: The region to validate
            
        Returns:
            Boolean indicating if region is valid
        """
        return region in self._data_manager.get_all_regions()

    def get_validation_error(self, infinitive: str, subject: str,
                           obj: Optional[str] = None, tense: Optional[str] = None,
                           aspect: Optional[str] = None) -> Optional[str]:
        """
        Get a descriptive error message for invalid inputs.
        
        Args:
            infinitive: The infinitive form
            subject: The subject marker
            obj: The object marker (optional)
            tense: The tense (optional)
            aspect: The aspect (optional)
            
        Returns:
            Error message string or None if all valid
        """
        if not self.validate_verb(infinitive):
            return f"Invalid verb: {infinitive}"
            
        if not self.validate_subject(subject):
            return f"Invalid subject: {subject}"
            
        if obj and not self.validate_object(obj):
            return f"Invalid object: {obj}"
            
        if not self.validate_combination(subject, obj):
            return f"Invalid subject-object combination: {subject}-{obj}"
            
        if not self.validate_verb_object_compatibility(infinitive, obj):
            return f"Verb {infinitive} cannot take object {obj}"
            
        if tense and not self.validate_tense(tense):
            return f"Invalid tense: {tense}"
            
        if aspect and not self.validate_aspect(aspect):
            return f"Invalid aspect: {aspect}"
            
        if aspect and not self.validate_aspect_compatibility(infinitive, aspect):
            return f"Verb {infinitive} does not support aspect {aspect}"
            
        return None