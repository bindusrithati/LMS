from enum import Enum, IntEnum


class GenderTypes(IntEnum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Roles(IntEnum):
    SuperAdmin = 99
    Admin = 2
    Student = 1


class OrderByTypes(str, Enum):
    ASC = "asc"
    DESC = "desc"


# 👇 ADD THIS
class Days(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
