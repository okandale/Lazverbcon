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
    def __init__(self, infinitive, present_third):
        self.infinitive = infinitive
        self.present_third = present_third
    
    


class ErgativeVerb(Verb):
    def accept_imperative_conjugator(self, imperative_visitor):
        imperative_visitor.conjugate_ergative_verb(self)
    
    def __str__(self):
        return (
            f"<ErgativeVerb infinitive=\"{self.infinitive}\" "
            f"third_person_form=\"{self.third_person_form}\">"
        )

class NominativeVerb(Verb):
    def accept_imperative_conjugator(self, imperative_visitor):
        imperative_visitor.conjugate_nominative_verb(self)

    def __str__(self):
        return (
            f"<NominativeVerb infinitive=\"{self.infinitive}\" "
            f"third_person_form=\"{self.third_person_form}\">"
        )

class DativeVerb(Verb):
    def accept_dative_conjugator(self, dative_conjugator):
        dative_conjugator.conjugate_dative_verb(self)

    def __str__(self):
        return (
            f"<DativeVerb infinitive=\"{self.infinitive}\" "
            f"third_person_form=\"{self.third_person_form}\">"
        )