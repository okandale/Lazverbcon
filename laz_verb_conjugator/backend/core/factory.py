from typing import Dict, Optional, Type
from .base import ConjugationBase
from ..handlers.ivd_handler import IVDHandler
from ..handlers.tve_handler import TVEHandler
from ..handlers.tvm_handler import TVMHandler
from .data_manager import VerbDataManager

class ConjugationFactory:
    """
    Factory class for creating and managing conjugator instances.
    Handles the creation of appropriate conjugators based on verb type and tense.
    """
    
    def __init__(self):
        self._data_manager = VerbDataManager()
        self._conjugator_cache: Dict[str, ConjugationBase] = {}
        self._handlers = {
            'IVD': IVDHandler(),
            'TVE': TVEHandler(),
            'TVM': TVMHandler()
        }
        self._tense_map = {
            'present': {
                'IVD': 'IVDPresentConjugator',
                'TVE': 'TVEPresentConjugator',
                'TVM': 'TVMPresentConjugator'
            },
            'past': {
                'IVD': 'IVDPastConjugator',
                'TVE': 'TVEPastConjugator',
                'TVM': 'TVMPastConjugator'
            },
            'future': {
                'IVD': 'IVDFutureConjugator',
                'TVE': 'TVEFutureConjugator',
                'TVM': 'TVMFutureConjugator'
            },
            'past_progressive': {
                'IVD': 'IVDPastProgressiveConjugator',
                'TVE': 'TVEPastProgressiveConjugator',
                'TVM': 'TVMPastProgressiveConjugator'
            }
        }

    def get_conjugator(self, verb: str, tense: str) -> Optional[ConjugationBase]:
        """
        Get appropriate conjugator for a verb and tense.
        
        Args:
            verb: The infinitive form of the verb
            tense: The desired tense
            
        Returns:
            Appropriate conjugator instance or None if not found
            
        Raises:
            ValueError: If verb type or tense is invalid
        """
        verb_type = self._data_manager.get_verb_type(verb)
        if not verb_type:
            raise ValueError(f"Unknown verb type for {verb}")
            
        if tense not in self._tense_map:
            raise ValueError(f"Invalid tense: {tense}")
            
        cache_key = f"{verb_type}_{tense}"
        
        # Return cached conjugator if available
        if cache_key in self._conjugator_cache:
            return self._conjugator_cache[cache_key]
            
        # Create new conjugator
        conjugator_class = self._get_conjugator_class(verb_type, tense)
        if not conjugator_class:
            return None
            
        handler = self._handlers.get(verb_type)
        if not handler:
            raise ValueError(f"No handler found for verb type: {verb_type}")
            
        conjugator = conjugator_class(handler)
        self._conjugator_cache[cache_key] = conjugator
        
        return conjugator

    def _get_conjugator_class(self, verb_type: str, tense: str) -> Optional[Type[ConjugationBase]]:
        """
        Get the conjugator class based on verb type and tense.
        
        Args:
            verb_type: The type of verb (IVD, TVE, or TVM)
            tense: The desired tense
            
        Returns:
            Conjugator class or None if not found
        """
        try:
            class_name = self._tense_map[tense][verb_type]
            module_name = f"lazuri.conjugators.{tense.lower()}"
            
            # Dynamic import
            import importlib
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (KeyError, ImportError, AttributeError):
            return None

    def clear_cache(self) -> None:
        """Clear the conjugator cache."""
        self._conjugator_cache.clear()

    def get_aspect_conjugator(self, verb: str, aspect: str) -> Optional[ConjugationBase]:
        """
        Get conjugator for specific aspects (potential, passive).
        
        Args:
            verb: The infinitive form of the verb
            aspect: The desired aspect ('potential' or 'passive')
            
        Returns:
            Appropriate conjugator instance or None if not found
            
        Raises:
            ValueError: If aspect is invalid
        """
        verb_type = self._data_manager.get_verb_type(verb)
        if not verb_type:
            raise ValueError(f"Unknown verb type for {verb}")

        aspect_map = {
            'potential': {
                'TVE': 'TVEPotentialConjugator',
                'TVM': 'TVMPotentialConjugator'
            },
            'passive': {
                'TVE': 'TVEPassiveConjugator',
                'TVM': 'TVMPassiveConjugator'
            }
        }

        if aspect not in aspect_map:
            raise ValueError(f"Invalid aspect: {aspect}")

        cache_key = f"{verb_type}_{aspect}"

        if cache_key in self._conjugator_cache:
            return self._conjugator_cache[cache_key]

        try:
            class_name = aspect_map[aspect].get(verb_type)
            if not class_name:
                return None

            module_name = f"lazuri.conjugators.{aspect.lower()}"
            module = importlib.import_module(module_name)
            conjugator_class = getattr(module, class_name)
            
            handler = self._handlers.get(verb_type)
            if not handler:
                raise ValueError(f"No handler found for verb type: {verb_type}")

            conjugator = conjugator_class(handler)
            self._conjugator_cache[cache_key] = conjugator
            
            return conjugator
        except (ImportError, AttributeError):
            return None

    def get_imperative_conjugator(self, verb: str, negative: bool = False) -> Optional[ConjugationBase]:
        """
        Get conjugator for imperative forms.
        
        Args:
            verb: The infinitive form of the verb
            negative: Whether to get negative imperative conjugator
            
        Returns:
            Appropriate conjugator instance or None if not found
        """
        verb_type = self._data_manager.get_verb_type(verb)
        if verb_type not in ['TVE', 'TVM']:
            return None

        cache_key = f"{verb_type}_{'negative_' if negative else ''}imperative"
        
        if cache_key in self._conjugator_cache:
            return self._conjugator_cache[cache_key]

        try:
            class_name = f"{verb_type}{'Negative' if negative else ''}ImperativeConjugator"
            module = importlib.import_module("lazuri.conjugators.imperative")
            conjugator_class = getattr(module, class_name)
            
            handler = self._handlers.get(verb_type)
            conjugator = conjugator_class(handler)
            self._conjugator_cache[cache_key] = conjugator
            
            return conjugator
        except (ImportError, AttributeError):
            return None

    def supports_aspect(self, verb: str, aspect: str) -> bool:
        """
        Check if a verb supports a specific aspect.
        
        Args:
            verb: The infinitive form of the verb
            aspect: The aspect to check
            
        Returns:
            Boolean indicating if aspect is supported
        """
        verb_type = self._data_manager.get_verb_type(verb)
        if not verb_type:
            return False

        aspect_support = {
            'potential': ['TVE', 'TVM'],
            'passive': ['TVE', 'TVM']
        }

        return verb_type in aspect_support.get(aspect, [])
    
    def get_imperative_conjugator(self, verb: str, negative: bool = False) -> Optional[ConjugationBase]:
        """Get conjugator for imperative forms."""
        verb_type = self._data_manager.get_verb_type(verb)
        if verb_type not in ['TVE', 'TVM']:
            return None
            
        cache_key = f"{verb_type}_{'negative_' if negative else ''}imperative"
        # Add imperative handling from old implementation