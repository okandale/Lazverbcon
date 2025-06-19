from typing import TYPE_CHECKING

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
        self.infinitive: str = infinitive
        self.present_third: str = present_third

    def accept_conjugator(self, _) -> str:
        raise NotImplementedError(
            "Please call this function from a concrete verb."
        )


class ErgativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator") -> str:
        return conjugator.conjugate_ergative_verb(self)

    def __str__(self):
        return (
            f'<ErgativeVerb infinitive="{self.infinitive}" '
            f'present_third="{self.present_third}">'
        )


class NominativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator") -> str:
        return conjugator.conjugate_nominative_verb(self)

    def __str__(self):
        return (
            f'<NominativeVerb infinitive="{self.infinitive}" '
            f'present_third="{self.present_third}">'
        )


class DativeVerb(Verb):
    def accept_conjugator(self, conjugator: "Conjugator"):
        return conjugator.conjugate_dative_verb(self)

    def __str__(self):
        return (
            f'<DativeVerb infinitive="{self.infinitive}" '
            f'present_third="{self.present_third}">'
        )
