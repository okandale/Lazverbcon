from .common import (
    PROTHETIC_CONSONANTS_FIRST_PERSON_BY_CLUSTER_AND_REGION,
    PROTHETIC_CONSONANTS_SECOND_PERSON_BY_CLUSTER,
    Person,
    Region,
    SuffixTable,
    extract_initial_cluster,
    extract_prefix,
)
from .verbs import Verb

PREVERB_HANDLERS = {}


def handle_preverb(preverb):
    def wrapper(func):
        PREVERB_HANDLERS[preverb] = func

    return wrapper


class Conjugator:
    def __init__(self, subject: Person, region: Region, object: Person = None):
        self.subject: Person = subject
        self.region: Region = region
        self.object: Person = object


    def conjugate(self, verb: Verb):
        return verb.accept_conjugator(self)

    def _conjugate(
        self,
        verb: Verb,
        prefix: str,
        suffixes: SuffixTable,
        starting_len=0,
        ending_len=0,
    ):
        extended_stem = verb.present_third[starting_len:-ending_len]

        stem = (
            extended_stem[len(prefix) :]
            if prefix is not None
            else extended_stem
        )
        conjugation = f"{stem}{suffixes[self.region][self.subject]}"
        if self.subject.is_first_person():
            conjugation = self.apply_epenthetic_segment(conjugation)

        # Put back the prefix if it exists.
        if prefix is not None:
            conjugation = f"{prefix}{conjugation}"
        return conjugation

    def _conjugate_nominative_verb(
        self,
        verb: Verb,
        suffix_table: SuffixTable,
        starting_len=0,
        ending_len=0,
    ) -> str:
        # Extract a potential verb prefix.
        prefix = extract_prefix(verb.infinitive)
        if prefix in PREVERB_HANDLERS:
            return PREVERB_HANDLERS[prefix](
                self, verb, prefix, suffix_table, starting_len, ending_len
            )
        else:
            return self._conjugate(
                verb, prefix, suffix_table, starting_len, ending_len
            )
    
    def conjugate_nominative_verb(self, _: Verb) -> str:
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )
    
    def conjugate_ergative_verb(self, _: Verb) -> str:
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )

    def conjugate_dative_verb(self, _: Verb) -> str:
        raise NotImplementedError(
            "Please call this method from a concrete conjugator."
        )

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


@handle_preverb("do")
def handle_do_prefix(
    conjugator: Conjugator,
    verb: Verb,
    prefix,
    suffix_table: SuffixTable,
    starting_len,
    ending_len,
):
    extended_stem = verb.present_third[starting_len:-ending_len]
    if verb.present_third.startswith("di"):
        if conjugator.subject.is_first_person():
            # Remove the first "d" before applying the epenthetic segment.
            stem = extended_stem[1:]
            conjugation = conjugator.apply_epenthetic_segment(
                stem + suffix_table[conjugator.region][conjugator.subject]
            )
            return f"do{conjugation}"
        else:
            stem = extended_stem
            conjugation = (
                stem + suffix_table[conjugator.region][conjugator.subject]
            )
        return conjugation
    else:
        return conjugator._conjugate(
            verb,
            prefix,
            suffix_table,
            starting_len=starting_len,
            ending_len=ending_len,
        )
