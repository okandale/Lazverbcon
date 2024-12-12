# lazuri/conjugators/base_conjugator.py

from typing import Dict, List, Optional, Tuple, Any
from ..core.base import ConjugationBase
from ..handlers.ivd_handler import IVDHandler
from ..handlers.tve_handler import TVEHandler
from ..handlers.tvm_handler import TVMHandler

class BaseVerbalConjugator:
    """Base class for all tense-specific conjugators."""
    
    def __init__(self, handler: ConjugationBase):
        self.handler = handler

    def _get_region_specific_suffix(self, subject: str, region: str) -> str:
        """Get region-specific suffix. To be implemented by derived classes."""
        raise NotImplementedError("Suffix handling must be implemented by tense-specific conjugators")

    def _handle_special_forms(self, infinitive: str, subject: str, region: str) -> Optional[str]:
        """Handle any special conjugation forms. To be implemented by derived classes."""
        return None

    def _modify_root_for_tense(self, root: str, subject: str) -> str:
        """Modify root based on tense-specific rules. To be implemented by derived classes."""
        return root

    def _validate_inputs(self, infinitive: str, subject: str, obj: Optional[str] = None,
                        applicative: bool = False, causative: bool = False) -> None:
        """Validate inputs before conjugation."""
        if not infinitive:
            raise ValueError("Infinitive form is required")
        if not subject:
            raise ValueError("Subject is required")
        if applicative and causative:
            raise ValueError("A verb cannot be both applicative and causative")
        if (applicative or causative) and not obj:
            raise ValueError("Object is required for applicative/causative forms")

    def conjugate(self, infinitive: str, subject: str, obj: Optional[str] = None,
                 applicative: bool = False, causative: bool = False,
                 use_optional_preverb: bool = False) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Base conjugation method that orchestrates the conjugation process.
        
        Args:
            infinitive: The infinitive form of the verb
            subject: The subject marker
            obj: The object marker (optional)
            applicative: Whether to use applicative form
            causative: Whether to use causative form
            use_optional_preverb: Whether to use optional preverb
            
        Returns:
            Dictionary mapping regions to lists of conjugation tuples
        """
        self._validate_inputs(infinitive, subject, obj, applicative, causative)
        
        # Get basic conjugation components from handler
        conjugation_data = self.handler.conjugate(infinitive, subject, obj,
                                                applicative, causative,
                                                use_optional_preverb)
        
        results: Dict[str, List[Tuple[str, str, str]]] = {}
        
        for region, forms in conjugation_data.items():
            if region not in results:
                results[region] = []
                
            for form_tuple in forms:
                subj, obj, components = form_tuple
                
                # Check for special forms first
                special_form = self._handle_special_forms(infinitive, subject, region)
                if special_form:
                    results[region].append((subj, obj, special_form))
                    continue
                
                # Unpack components
                if isinstance(components, tuple):
                    prefix = components[0]
                    root = components[1]
                    preverb = components[2]
                    # Some handlers might include additional components
                    extra_components = components[3:] if len(components) > 3 else []
                else:
                    prefix = components
                    root = ""
                    preverb = ""
                    extra_components = []
                
                # Modify root based on tense rules
                root = self._modify_root_for_tense(root, subject)
                
                # Get tense and region specific suffix
                suffix = self._get_region_specific_suffix(subject, region)
                
                # Combine components
                if extra_components:
                    # Handle any extra components (e.g., aspect markers)
                    conjugated = f"{prefix}{root}{''.join(extra_components)}{suffix}"
                else:
                    conjugated = f"{prefix}{root}{suffix}"
                
                results[region].append((subj, obj, conjugated.strip()))
        
        return results