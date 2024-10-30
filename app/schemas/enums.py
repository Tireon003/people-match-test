from enum import Enum


class OrderBy(str, Enum):
    reg_date = 'registration_date'


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class Distance(str, Enum):
    km1 = 1
    km2 = 2
    km5 = 5
    km10 = 10
    km20 = 20
    km50 = 50
    km100 = 100
