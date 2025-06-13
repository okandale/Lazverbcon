from .common import (PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION,
                     PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER, Person,
                     extract_initial_cluster)


class Conjugator:
    def __init__(self, subject: Person, region, object: Person = None):
        self.subject = subject
        self.region = region
        self.object = object

    def apply_prothesis(self, inflected_stem):
        """Apply a prothetic consonant to the inflected stem if required.

        This method inserts a consonant at the beginning of the verb form
        according to phonological rules specific to the grammatical person and region.
        The phenomenon is known as *prothesis*, and is used in Laz to ease pronunciation,
        especially in first and second person conjugations.

        The inserted consonant (e.g., 'p', 'v', 'b', 'm', etc.) depends on the initial
        consonant cluster of the verb stem and may vary across dialectal regions.

        Example:
            'skidu' → 'pskidu' (with 'p' as the prothetic consonant)
            'isinapam' → 'visinapam' (for vowel-initial stems)

        Args:
            inflected_stem (str): The already-inflected verb stem, before any prothesis.

        Returns:
            str: The verb form with the appropriate prothetic consonant, if applicable.
                Returns the original stem if no prothesis rule matches.
        """
        prothetic_consonants_by_cluster = (
            PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION[
                self.region
            ]
            if self.subject.is_first_person()
            else PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER
        )

        # Prefixes are a dictionary of lists of clusters. Loop to seek
        # our cluster.
        initial_cluster = extract_initial_cluster(inflected_stem)
        for (
            prothesis,
            initial_clusters,
        ) in prothetic_consonants_by_cluster.items():
            if initial_cluster in initial_clusters:
                # We have found the initial cluster referring to our prothesis,
                # so we apply the prothesis and return the result.
                return f"{prothesis}{inflected_stem}"
