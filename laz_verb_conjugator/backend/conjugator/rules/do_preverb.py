from typing import TYPE_CHECKING

from ..common import Person, Region
from ..verbs import Verb

if TYPE_CHECKING:
    from ..conjugator import Conjugator


APPLICATIVE_PREFIXES = {
    Person.FIRST_SINGULAR: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "dovi",
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "dovi",
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "dobi",
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "dovi",
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
    },
    Person.SECOND_SINGULAR: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "dogi",
            Person.SECOND_SINGULAR: "di",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "dogi",
            Person.SECOND_SINGULAR: "di",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "dogi",
            Person.SECOND_SINGULAR: "di",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "dogi",
            Person.SECOND_SINGULAR: "di",
            Person.THIRD_SINGULAR: "dogi",
            Person.SECOND_PLURAL: "dogi",
            Person.THIRD_PLURAL: "dogi",
        },
    },
    Person.THIRD_SINGULAR: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "dobu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dobu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
    },
    Person.FIRST_PLURAL: {
        Region.ARDESEN: {
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.FIRST_PLURAL: "dovi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.PAZAR: {
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.FIRST_PLURAL: "dovi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.FIRST_PLURAL: "dobi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
        Region.HOPA: {
            Person.SECOND_SINGULAR: "domi",
            Person.THIRD_SINGULAR: "domi",
            Person.FIRST_PLURAL: "dovi",
            Person.SECOND_PLURAL: "domi",
            Person.THIRD_PLURAL: "domi",
        },
    },
    Person.SECOND_PLURAL: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "dogi",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.SECOND_PLURAL: "di",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "dogi",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.SECOND_PLURAL: "di",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "dogi",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.SECOND_PLURAL: "di",
            Person.THIRD_PLURAL: "dogi",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "dogi",
            Person.THIRD_SINGULAR: "dogi",
            Person.FIRST_PLURAL: "dogi",
            Person.SECOND_PLURAL: "di",
            Person.THIRD_PLURAL: "dogi",
        },
    },
    Person.THIRD_PLURAL: {
        Region.ARDESEN: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.PAZAR: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.FINDIKLI_ARHAVI: {
            Person.FIRST_SINGULAR: "dobu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dobu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
        Region.HOPA: {
            Person.FIRST_SINGULAR: "dovu",
            Person.SECOND_SINGULAR: "du",
            Person.THIRD_SINGULAR: "du",
            Person.FIRST_PLURAL: "dovu",
            Person.SECOND_PLURAL: "du",
            Person.THIRD_PLURAL: "du",
        },
    },
}
