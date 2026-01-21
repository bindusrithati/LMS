# app/utils/mapper.py
from typing import Any


class Mapper:
    def to(self, cls: Any) -> "Mapper":
        return self

    def map(self, data: Any) -> Any:
        return data


mapper: Mapper = Mapper()
