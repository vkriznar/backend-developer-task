import enum


class NoteType(enum.Enum):
    TEXT = "TEXT"
    LIST = "LIST"


class SharedType(enum.Enum):
    NONE = "NONE"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class HeadingSort(enum.Enum):
    NONE = "NONE"
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
