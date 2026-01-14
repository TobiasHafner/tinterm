from __future__ import annotations

from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from .attributes import StyleKey


class StyledString:
    __slots__ = ("_text", "_style")

    def __init__(self, text: str, style: dict[StyleKey, Any] | None = None):
        self._text = str(text)
        self._style = MappingProxyType(dict(style) if style else {})

    @property
    def text(self) -> str:
        return self._text

    @property
    def style(self) -> Mapping[StyleKey, Any]:
        return self._style

    def __len__(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return self._text

    def __add__(self, other: object) -> StyledText:
        from .styled import StyledText

        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        from .styled import StyledText

        return StyledText._from_parts(other, self)


class StyledText:
    __slots__ = ("_parts",)

    def __init__(self, parts: Iterable[StyledString]):
        self._parts = tuple(parts)

    @staticmethod
    def _from_parts(left: object, right: object) -> StyledText:
        parts: list[StyledString] = []

        def add(value: object):
            if isinstance(value, StyledText):
                parts.extend(value._parts)  # safe: tuple
            elif isinstance(value, StyledString):
                parts.append(value)
            else:
                parts.append(StyledString(str(value)))

        add(left)
        add(right)
        return StyledText(parts)

    @property
    def parts(self) -> Sequence[StyledString]:
        return self._parts

    def __len__(self) -> int:
        return sum(len(p) for p in self._parts)

    def __iter__(self):
        return iter(self._parts)

    def __add__(self, other: object) -> StyledText:
        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        return StyledText._from_parts(other, self)

    def __str__(self) -> str:
        return "".join(p.text for p in self._parts)
