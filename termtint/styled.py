from __future__ import annotations
from typing import Any

from .attributes import Color, Modifier, StyleKey

class StyledString(str):
    __slots__ = ("_style",)

    def __new__(cls, text: str, style: dict[str, Any] | None = None):
        obj = super().__new__(cls, text)
        obj._style = style or {}
        return obj

    @property
    def style(self) -> dict[StyleKey, Any]:
        return self._style

    def __add__(self, other: object) -> StyledText:
        from .styled import StyledText
        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        from .styled import StyledText
        return StyledText._from_parts(other, self)

    def __getitem__(self, key):
        result = super().__getitem__(key)
        return StyledString(result, style=dict(self._style))

_string_methods = [
    "upper", "lower", "capitalize", "title", "casefold", "swapcase",
    "center", "ljust", "rjust", "zfill",
    "strip", "lstrip", "rstrip",
    "replace", "translate",
    "join",
    "partition", "rpartition",
    "split", "rsplit", "splitlines",
    "expandtabs",
    "format", "format_map",
]

def _wrap_string_method(method_name: str):
    def wrapper(self: StyledString, *args, **kwargs):
        result = getattr(str, method_name)(self, *args, **kwargs)
        if isinstance(result, str):
            return StyledString(result, style=dict(self._style))
        if isinstance(result, list):
            return [StyledString(s, style=dict(self._style)) if isinstance(s, str) else s for s in result]
        if isinstance(result, tuple):
            return tuple(StyledString(s, style=dict(self._style)) if isinstance(s, str) else s for s in result)
        return result
    return wrapper

for method in _string_methods:
    setattr(StyledString, method, _wrap_string_method(method))

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
        return sum(len(p) for p in self.parts)

    def __iter__(self):
        yield from self.parts

    def __add__(self, other: object) -> StyledText:
        return StyledText._from_parts(self, other)

    def __radd__(self, other: object) -> StyledText:
        return StyledText._from_parts(other, self)

    def __getitem__(self, key):
        if isinstance(key, slice):
            new_parts = []
            start, stop, step = key.indices(len(self))
            current_index = 0
            for part in self.parts:
                part_len = len(part)
                part_start = max(0, start - current_index)
                part_stop = max(0, min(part_len, stop - current_index))
                if part_start < part_stop:
                    new_parts.append(part[part_start:part_stop])
                current_index += part_len
                if current_index >= stop:
                    break
            return StyledText(new_parts)

        # Single-character access
        index = key if key >= 0 else len(self) + key
        current_index = 0
        for part in self.parts:
            if current_index + len(part) > index:
                return part[index - current_index]
            current_index += len(part)
        raise IndexError("StyledText index out of range")

    def upper(self):
        return StyledText([p.upper() for p in self.parts])

    def lower(self):
        return StyledText([p.lower() for p in self.parts])

    def capitalize(self):
        if not self.parts:
            return StyledText([])
        return StyledText([self.parts[0].capitalize()] + self.parts[1:])

    def title(self):
        return StyledText([p.title() for p in self.parts])

    def __str__(self) -> str:
        return "".join(str(p) for p in self.parts)

