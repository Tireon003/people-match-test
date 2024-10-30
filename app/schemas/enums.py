from enum import Enum


class OrderBy(str, Enum):
    reg_date = 'registration_date'


class Gender(str, Enum):
    male = 'male'
    female = 'female'
