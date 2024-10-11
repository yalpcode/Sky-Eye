from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter


@unique
class BaseEnum(Enum):
    @classmethod
    @lru_cache(None)
    def values(cls) -> tuple:
        return tuple(map(attrgetter('value'), cls))


class ResponseStatusCodeEnum(BaseEnum):
    SUCCESS = 1001

    REPORT_DUPLICATED = 2001

    ERROR_DIFFERENT_CONTENT = 3001
    ERROR_UPLOAD = 3002
    ERROR_INSERT = 3003


class ResponseStatusDescriptionEnum(BaseEnum):
    SUCCESS = 'Success'
    REPORT_DUPLICATED = 'Report has duplicate on the server'
    ERROR_DIFFERENT_CONTENT = 'Report has duplicate on the server, but with different content'
    ERROR_UPLOAD = 'Report not uploaded'
    ERROR_INSERT = 'Report cant be inserted!'
