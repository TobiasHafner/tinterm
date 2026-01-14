# Copyright 2026 Tobias Hafner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import deque
from typing import Union

from .attributes import Color, Modifier, StyleKey
from .styled import StyledString, StyledText

_ENABLED: bool = True
_EXTRACTORS = [
    (
        StyleKey.FOREGROUND,
        lambda c: str(c.value.foreground) if isinstance(c, Color) else None,
    ),
    (
        StyleKey.BACKGROUND,
        lambda c: str(c.value.background) if isinstance(c, Color) else None,
    ),
    (
        StyleKey.MODIFIERS,
        lambda mods: (
            [str(m.value) for m in mods if isinstance(m, Modifier)] if mods else []
        ),
    ),
]


def enable_colors():
    global _ENABLED
    _ENABLED = True


def disable_colors():
    global _ENABLED
    _ENABLED = False


def _render_no_color(value: Union[StyledString, StyledText]) -> str:
    stack = deque([value])
    result: list[str] = []

    while stack:
        v = stack.popleft()
        if isinstance(v, StyledText):
            stack.extendleft(reversed(v.parts))
        else:
            result.append(str(v))

    return "".join(result)


def render(value: Union[StyledString, StyledText]) -> str:
    if not _ENABLED:
        return _render_no_color(value)

    stack = deque([value])
    result: list[str] = []

    while stack:
        v = stack.popleft()
        if isinstance(v, StyledText):
            stack.extendleft(reversed(v.parts))
            continue

        text = str(v)
        codes: list[str] = []

        for key, extractor in _EXTRACTORS:
            val = v.style.get(key)
            res = extractor(val)
            if isinstance(res, list):
                codes.extend(res)
            elif res:
                codes.append(res)

        if codes:
            result.append(f"\033[{';'.join(codes)}m{text}\033[0m")
        else:
            result.append(text)

    return "".join(result)
