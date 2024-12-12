# lazuri/conjugators/present.py

from typing import Dict, List, Tuple, Optional
from ..core.base import ConjugationBase
from ..core.validator import ConjugationValidator

class IVDPresentConjugator(ConjugationBase):
    """Conjugator for IVD verbs in present tense."""

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.validator = ConjugationValidator()

    def get_suffixes(self, region: str) -> Dict[str, str]:
        """Get the present tense suffixes for IVD verbs."""
        return {
            'S1_Singular': '',
            'S2_Singular': '',
            'S3_Singular': 's',
            'S1_Plural': 't',
            'S2_Plural': 't',
            'S3_Plural': 'an'
        }

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Conjugate IVD verb in present tense.
        
        Args:
            infinitive: The infinitive form
            subject: The subject marker
            obj: The object marker (not used for IVD)
            applicative: Whether to use applicative form
            causative: Whether to use causative form
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to conjugation tuples
        """
        # Validate inputs
        error = self.validator.get_validation_error(infinitive, subject, obj)
        if error:
            raise ValueError(error)

        if obj:
            raise ValueError("IVD verbs cannot take objects")

        if applicative or causative:
            raise ValueError("IVD verbs cannot be applicative or causative")

        result = {}
        verb_data, regions = self.data_manager.get_verb_data(infinitive)
        
        for region in regions:
            result[region] = []
            for verb_form, _ in verb_data:
                # Process the verb
                root = self.process_compound_verb(verb_form)
                first_word = self.get_first_word(verb_form)

                # Get preverb if any
                preverb = self.extract_preverb(root)
                if preverb:
                    root = root[len(preverb):]

                # Handle special cases
                root = self.handle_special_case_u(root, subject, preverb)

                # Get the appropriate suffix
                suffix = self.get_suffixes(region)[subject]

                # Handle preverb modifications
                if preverb:
                    preverb_form = self.get_preverb_form(preverb, subject)
                    conjugated = f"{preverb_form}{root}{suffix}"
                else:
                    # Get subject marker
                    marker = self.get_subject_marker(subject)
                    conjugated = f"{marker}{root}{suffix}"

                result[region].append((subject, None, f"{first_word} {conjugated}".strip()))

        return result

class TVEPresentConjugator(ConjugationBase):
    """Conjugator for TVE verbs in present tense."""

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.validator = ConjugationValidator()

    def get_suffixes(self, region: str) -> Dict[str, str]:
        """Get the present tense suffixes for TVE verbs."""
        return {
            'S1_Singular': '',
            'S2_Singular': '',
            'S3_Singular': 's',
            'S1_Plural': 't',
            'S2_Plural': 't',
            'S3_Plural': 'an'
        }

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Conjugate TVE verb in present tense.
        
        Args:
            infinitive: The infinitive form
            subject: The subject marker
            obj: The object marker
            applicative: Whether to use applicative form
            causative: Whether to use causative form
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to conjugation tuples
        """
        # Validate inputs
        error = self.validator.get_validation_error(infinitive, subject, obj)
        if error:
            raise ValueError(error)

        result = {}
        verb_data, regions = self.data_manager.get_verb_data(infinitive)

        for region in regions:
            result[region] = []
            for verb_form, _ in verb_data:
                # Process the verb
                root = self.process_compound_verb(verb_form)
                first_word = self.get_first_word(verb_form)

                # Get preverb if any
                preverb = self.extract_preverb(root)
                if preverb:
                    root = root[len(preverb):]

                # Handle markers (applicative/causative)
                if applicative and causative:
                    marker = self.handle_double_marker(root, obj)
                elif applicative:
                    marker = self.handle_applicative_marker(root, obj)
                elif causative:
                    marker = self.handle_causative_marker(root, obj)
                else:
                    marker = ''

                # Apply marker to root
                if marker:
                    root = marker + root

                # Get the appropriate suffix
                suffix = self.get_suffixes(region)[subject]

                # Handle object-specific modifications
                if obj:
                    root, suffix = self.handle_object_modifications(root, suffix, obj, subject)

                # Handle preverb and subject marker
                prefix = self.handle_prefix(preverb, subject, obj, root, region)

                conjugated = f"{prefix}{root}{suffix}"
                result[region].append((subject, obj, f"{first_word} {conjugated}".strip()))

        return result


class TVMPresentConjugator(ConjugationBase):
    """Conjugator for TVM verbs in present tense."""

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.validator = ConjugationValidator()

    def get_suffixes(self, region: str) -> Dict[str, str]:
        """Get the present tense suffixes for TVM verbs."""
        return {
            'S1_Singular': 'r',
            'S2_Singular': 'r',
            'S3_Singular': 'n',
            'S1_Plural': 'rt',
            'S2_Plural': 'rt',
            'S3_Plural': 'nan'
        }

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Conjugate TVM verb in present tense.
        
        Args:
            infinitive: The infinitive form
            subject: The subject marker
            obj: The object marker (not used for TVM)
            applicative: Whether to use applicative form
            causative: Whether to use causative form
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to conjugation tuples
        """
        # Validate inputs
        error = self.validator.get_validation_error(infinitive, subject, obj)
        if error:
            raise ValueError(error)

        if obj:
            raise ValueError("TVM verbs cannot take objects")

        result = {}
        verb_data, regions = self.data_manager.get_verb_data(infinitive)

        for region in regions:
            result[region] = []
            for verb_form, _ in verb_data:
                # Process the verb
                root = self.process_compound_verb(verb_form)
                first_word = self.get_first_word(verb_form)

                # Get preverb if any
                preverb = self.extract_preverb(root)
                if preverb:
                    root = root[len(preverb):]

                # Get the appropriate suffix
                suffix = self.get_suffixes(region)[subject]

                # Handle preverb modifications
                if preverb:
                    preverb_form = self.get_preverb_form(preverb, subject)
                    conjugated = f"{preverb_form}{root}{suffix}"
                else:
                    # Handle TVM-specific subject marking
                    marker = self.handle_tvm_subject_marker(subject, root)
                    conjugated = f"{marker}{root}{suffix}"

                result[region].append((subject, None, f"{first_word} {conjugated}".strip()))

        return result