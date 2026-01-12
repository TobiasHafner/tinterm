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
    
    def upper(self):
        return StyledString(super().upper(), style=dict(self._style))

    def lower(self):
        return StyledString(super().lower(), style=dict(self._style))

    def title(self):
        return StyledString(super().title(), style=dict(self._style))

    def capitalize(self):
        return StyledString(super().capitalize(), style=dict(self._style))

class StyledText:
    __slots__ = ("parts",)

    def __init__(self, parts: list[StyledString]):
        self.parts = parts
    
    def __len__(self) -> int:
        return sum(len(p) for p in self.parts)

    def __iter__(self):
        for part in self.parts:
            yield part

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
       
        # Return single-character StyledString
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
        from .render import render
        return render(self)

