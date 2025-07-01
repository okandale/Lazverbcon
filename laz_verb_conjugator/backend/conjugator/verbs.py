from typing import TYPE_CHECKING, List

from .common import extract_preverb

if TYPE_CHECKING:
    from .conjugator import Conjugator


class Verb:
    """Represents a Laz verb with its base forms.

    This class stores the key morphological forms of a Laz verb needed
    for conjugation and morphological analysis.

    Attributes:
        infinitive (str): The infinitive form of the verb, typically
            ending in -u. It consists of a verbal prefix, a stem, and an
            infinitive suffix (e.g., 'oskidu').

        present_third (str): The third person singular present tense form of
            the verb. This form is used to extract the stem and identify
            inflectional patterns for conjugating into other tenses or
            moods (e.g., 'skidun').
    """

    def __init__(self, infinitive: str, present_third: str):
        self._infinitive: str = infinitive
        self._present_third: str = present_third

        infinitive_elements = self._process_compound_verb(infinitive)

        if len(infinitive_elements) > 1:
            self.complement = infinitive_elements[0]
            self.infinitive = infinitive_elements[1]
        else:
            self.complement = None
            self.infinitive = infinitive_elements[0]

        present_third_elements = self._process_compound_verb(present_third)
        if len(present_third_elements) > 1:
            self.present_third = present_third_elements[1]
        else:
            self.present_third = present_third_elements[0]

        self.preverb: str = extract_preverb(self.infinitive)
        self.is_preverb_mutated: bool = (
            True
            if extract_preverb(self.present_third) != self.preverb
            else False
        )
        self.stem: str = self._extract_stem()
        [self.prefix, self.suffix] = self._extract_affixes()

    def finalize_conjugation(self, conjugation):
        """Put back the complement, if it exists."""
        return (
            f"{self.complement} {conjugation}"
            if self.complement is not None
            else conjugation
        )

    def _process_compound_verb(self, verb) -> List[str]:
        """Process compound verbs. If they are so, return the complement and
        the actual verb.

        """
        if " " in verb:
            complement, *verbs_part = verb.split(" ")
            return [complement, " ".join(verbs_part)]
        else:
            return [verb]

    def accept_conjugator(self, _) -> str:
        raise NotImplementedError(
            "Please call this function from a concrete verb."
        )

    def _extract_stem(self) -> str:
        """Get the stem of the verb.

        The actual stem of the verb will be useful for conjugations among
        tenses and moods.

        If the verb is a prefixed one, remove it. Otherwise, remove the o-.

        If the infinitive ends with -u, remove it too.

        You may want to override this method if you have a special case.
        """
        if self.preverb is not None:
            stem = self.infinitive[len(self.preverb) :]  # Removed the prefix.
        elif self.infinitive.startswith("o"):
            stem = self.infinitive[1:]  # Remove the prepending "o".
        else:
            stem = self.infinitive  # XXX: How do we handle these cases?

        # Now, remove the trailing -u if it exists.
        if stem.endswith("u"):
            stem = stem[:-1]
        return stem

    def _extract_affixes(self) -> List[str]:
        """Extract the affixes of the verb.

        As we know the stem and the third person form, we will be able to
        extract these affixes from the latter.

        Example: if we have osinapu/isinapams, the stem will be "sinap".

        Then the prefix will be "i" and the suffix "ams".
        """
        stem_position = self.present_third.find(self.stem)
        prefix = self.present_third[:stem_position]
        suffix = self.present_third[stem_position + len(self.stem) :]
        return prefix, suffix


class ErgativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator") -> str:
        return conjugator.conjugate_ergative_verb(self)

    def __str__(self):
        return (
            f'<ErgativeVerb infinitive="{self._infinitive}" '
            f'present_third="{self._present_third}" '
            f'preverb="{self.preverb}" '
            f'stem="{self.stem}" '
            f'prefix="{self.prefix}" '
            f'suffix="{self.suffix}">'
        )


class NominativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator") -> str:
        return conjugator.conjugate_nominative_verb(self)

    def __str__(self):
        return (
            f'<NominativeVerb infinitive="{self.infinitive}" '
            f'present_third="{self.present_third}" '
            f'preverb="{self.preverb}" '
            f'stem="{self.stem}" '
            f'prefix="{self.prefix}" '
            f'suffix="{self.suffix}">'
        )


class DativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator"):
        return conjugator.conjugate_dative_verb(self)

    def __str__(self):
        return (
            f'<DativeVerb infinitive="{self.infinitive}" '
            f'present_third="{self.present_third}" '
            f'preverb="{self.preverb}" '
            f'stem="{self.stem}" '
            f'prefix="{self.prefix}" '
            f'suffix="{self.suffix}">'
        )
