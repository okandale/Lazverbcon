from enum import IntFlag

class Mood(IntFlag):
    APPLICATIVE = 1
    CAUSATIVE = 2
    OPTATIVE = 4
    IMPERATIVE = 8
    NEGATIVE_IMPERATIVE = 16


def check_flags(flags):
    if Mood.IMPERATIVE | Mood.NEGATIVE_IMPERATIVE in flags:
        raise Exception(
            "The 'imperative' and 'negative imperative' modes are "
            "exclusive. Please select only one of them, or not at all."
        )
