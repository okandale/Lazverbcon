from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conjugator import Conjugator

from backend.conjugator.verbs import Verb

from .common import (Person, Region, RegionSuffixTable, SuffixTable,
                     extract_prefix)


class ConjugateErgativeVerbMixin:
    def conjugate_ergative_verb(
        self: "Conjugator",
        verb: Verb,
        suffix_table: SuffixTable,
        ending_len: int,
    ):
        prefix = extract_prefix(verb.infinitive)
        extended_stem = verb.present_third[:-ending_len]
        stem = (
            extended_stem[len(prefix) :]
            if prefix is not None
            else extended_stem
        )
        conjugation = f"{stem}{suffix_table[self.subject]}"
        if self.subject.is_first_person() or self.object is not None:
            conjugation = self.apply_epenthetic_segment(conjugation)
        # Put back the prefix if it exists.
        if prefix is not None:
            conjugation = f"{prefix}{conjugation}"
        return conjugation
