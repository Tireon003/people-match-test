from enum import Enum


class Gender(str, Enum):
    male: str = 'male'
    female: str = 'female'
