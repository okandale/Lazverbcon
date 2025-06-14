from .common import (
    PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION,
    PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER,
    Person,
    extract_initial_cluster,
)


class Conjugator:
    def __init__(self, subject: Person, region, object: Person = None):
        self.subject = subject
        self.region = region
        self.object = object

    def apply_epenthetic_segment(self, inflected_stem):
        """
        Apply an epenthetic segment to the inflected stem if required.

        This method inserts a consonantal segment at the beginning of the verb form
        according to phonological and morphological rules specific to the grammatical
        person and dialectal region.

        The inserted segment—commonly referred to as an *epenthetic segment*—serves to
        ease articulation or mark person agreement in certain Laz verb conjugations.
        It is typically inserted in first and second person forms when the stem
        begins with specific consonant clusters or vowels.

        Example:
            'skidu' → 'pskidu' (with 'p' as the epenthetic segment)
            'isinapam' → 'visinapam' (vowel-initial stem, epenthetic 'v')

        Args:
            inflected_stem (str): The already-inflected verb stem, before any epenthetic insertion.

        Returns:
            str: The verb form with the appropriate epenthetic segment, if applicable.
                Returns the original stem if no rule matches.
        """
        epenthetic_segments_by_cluster = (
            PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION[
                self.region
            ]
            if self.subject.is_first_person()
            else PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER
        )

        initial_cluster = extract_initial_cluster(inflected_stem)
        for (
            epenthetic_segment,
            initial_clusters,
        ) in epenthetic_segments_by_cluster.items():
            if initial_cluster in initial_clusters:
                return (
                    f"{epenthetic_segment}{inflected_stem}"
                    if epenthetic_segment != initial_cluster
                    else inflected_stem
                )
