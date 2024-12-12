import pandas as pd
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path

class VerbDataManager:
    """
    Centralizes data loading and management for verb conjugation.
    Implements singleton pattern to ensure single data source.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VerbDataManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.verbs: Dict[str, List[Tuple[str, str]]] = {}
            self.regions: Dict[str, List[str]] = {}
            self.verb_types: Dict[str, str] = {}
            self.cached_forms: Dict[str, Dict[str, Set[str]]] = {}
            self._initialized = True

    def load_data(self, filepath: str) -> None:
        """
        Load verb data from CSV file.
        
        Args:
            filepath: Path to the CSV file containing verb data
        
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If required columns are missing
        """
        try:
            df = pd.read_csv(filepath)
            required_columns = [
                'Laz Infinitive', 'Category',
                'Laz 3rd Person Singular Present',
                'Region'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            # Process each verb entry
            for _, row in df.iterrows():
                infinitive = row['Laz Infinitive'].lower()
                
                # Get all present forms (main and alternatives)
                present_forms = []
                for col in ['Laz 3rd Person Singular Present',
                          'Laz 3rd Person Singular Present Alternative 1',
                          'Laz 3rd Person Singular Present Alternative 2']:
                    if col in df.columns and pd.notna(row[col]):
                        present_forms.append(row[col])

                # Get all regions (main and alternatives)
                regions = []
                for col in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
                    if col in df.columns and pd.notna(row[col]):
                        regions.extend([r.strip() for r in str(row[col]).split(',')])

                # Store the data
                self.verbs[infinitive] = []
                for form in present_forms:
                    self.verbs[infinitive].append((form, ','.join(regions)))
                
                self.regions[infinitive] = list(set(regions)) or ["All"]
                self.verb_types[infinitive] = row['Category']

        except FileNotFoundError:
            raise FileNotFoundError(f"Verb data file not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error loading verb data: {str(e)}")

    def get_verb_data(self, infinitive: str) -> Tuple[Optional[List[Tuple[str, str]]], Optional[List[str]]]:
        """
        Get verb forms and regions for a given infinitive.
        
        Args:
            infinitive: The infinitive form of the verb
            
        Returns:
            Tuple containing list of verb forms and list of regions
        """
        infinitive = infinitive.lower()
        return self.verbs.get(infinitive), self.regions.get(infinitive)

    def get_verb_type(self, infinitive: str) -> Optional[str]:
        """
        Get the type (category) of a verb.
        
        Args:
            infinitive: The infinitive form of the verb
            
        Returns:
            String indicating verb type (IVD, TVE, or TVM)
        """
        return self.verb_types.get(infinitive.lower())

    def verify_verb_exists(self, infinitive: str) -> bool:
        """
        Check if a verb exists in the database.
        
        Args:
            infinitive: The infinitive form of the verb
            
        Returns:
            Boolean indicating if verb exists
        """
        return infinitive.lower() in self.verbs

    def get_all_verbs_by_type(self, verb_type: str) -> List[str]:
        """
        Get all verbs of a specific type.
        
        Args:
            verb_type: The type of verbs to retrieve (IVD, TVE, or TVM)
            
        Returns:
            List of infinitive forms
        """
        return [inf for inf, type_ in self.verb_types.items() if type_ == verb_type]

    def get_all_regions(self) -> Set[str]:
        """
        Get all unique regions across all verbs.
        
        Returns:
            Set of unique region names
        """
        regions = set()
        for region_list in self.regions.values():
            regions.update(region_list)
        return regions

    def cache_conjugated_form(self, infinitive: str, tense: str, conjugated_form: str) -> None:
        """
        Cache a conjugated form for faster lookup.
        
        Args:
            infinitive: The infinitive form of the verb
            tense: The tense of conjugation
            conjugated_form: The conjugated form to cache
        """
        if infinitive not in self.cached_forms:
            self.cached_forms[infinitive] = {}
        if tense not in self.cached_forms[infinitive]:
            self.cached_forms[infinitive][tense] = set()
        self.cached_forms[infinitive][tense].add(conjugated_form)

    def get_cached_forms(self, infinitive: str, tense: str) -> Optional[Set[str]]:
        """
        Retrieve cached conjugated forms.
        
        Args:
            infinitive: The infinitive form of the verb
            tense: The tense of conjugation
            
        Returns:
            Set of cached conjugated forms or None if not cached
        """
        return self.cached_forms.get(infinitive, {}).get(tense)

    def clear_cache(self) -> None:
        """Clear all cached conjugated forms."""
        self.cached_forms.clear()