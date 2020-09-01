from typing import Optional

GENDER_MAP = {
    1: 'male',
    2: 'female',
    3: 'undesignated',
}


def gender_hru(gender: list) -> Optional[str]:
    return GENDER_MAP.get(gender)


def validate_gender(text: str) -> Optional[int]:
    try:
        gender = int(text)
    except (TypeError, ValueError):
        return None

    if gender < 0 or gender > 3:
        return None
    return gender


def validate_age(text: str) -> Optional[int]:
    try:
        age = int(text)
    except (TypeError, ValueError):
        return None

    if age < 0 or age > 100:
        return None
    return age
