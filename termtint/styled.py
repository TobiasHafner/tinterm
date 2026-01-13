from __future__ import annotations
from typing import Any

from .attributes import StyleKey

class StyledString:
    __slots__ = ("text", "_style")

    def __init__(self, text: str, style: dict[StyleKey, Any] | None = None):
        self.text = text
        self._style = style or {}

    @property
    def style(self) -> dict[StyleKey, Any]:
        return self._style

    def __len__(self) -> int:
        return len(self.text)

    def __str__(self) -> str:
        return self.text
    
    def __add__(self, other: object) -> StyledText:
        from .styled import StyledText
        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        from .styled import StyledText
        return StyledText._from_parts(other, self)

class StyledText:
    __slots__ = ("_parts",)

    def __init__(self, parts: list[StyledString]):
        self._parts = parts

    @staticmethod
    def _from_parts(left: object, right: object) -> StyledText:
        parts: list[StyledString] = []

        def add(value: object):
            if isinstance(value, StyledText):
                parts.extend(value.parts)
            elif isinstance(value, StyledString):
                parts.append(value)
            else:
                parts.append(StyledString(str(value)))

        add(left)
        add(right)
        return StyledText(parts)

    @property
    def parts(self) -> list[StyledString]:
        return self._parts

    def __len__(self) -> int:
        return sum(len(p) for p in self._parts)

    def __iter__(self):
        yield from self._parts

    def __add__(self, other: object) -> StyledText:
        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        return StyledText._from_parts(other, self)
    
    def __str__(self) -> str:
        return "".join(p.text for p in self._parts)

