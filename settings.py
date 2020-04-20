from enum import Enum, auto

class Verbose(Enum):
    FULL = 0,
    PARTIAL = 1,
    CRITICAL = 2,
    NONE = 3