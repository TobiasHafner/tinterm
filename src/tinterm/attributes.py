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

from dataclasses import dataclass
from enum import Enum, IntEnum


class Modifier(IntEnum):
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    STRIKETHROUGH = 9


@dataclass(frozen=True)
class AnsiColor:
    foreground: int
    background: int


class Color(Enum):
    BLACK = AnsiColor(30, 40)
    RED = AnsiColor(31, 41)
    GREEN = AnsiColor(32, 42)
    YELLOW = AnsiColor(33, 43)
    BLUE = AnsiColor(34, 44)
    MAGENTA = AnsiColor(35, 45)
    CYAN = AnsiColor(36, 46)
    WHITE = AnsiColor(37, 47)

    BRIGHT_BLACK = AnsiColor(90, 100)
    BRIGHT_RED = AnsiColor(91, 101)
    BRIGHT_GREEN = AnsiColor(92, 102)
    BRIGHT_YELLOW = AnsiColor(93, 103)
    BRIGHT_BLUE = AnsiColor(94, 104)
    BRIGHT_MAGENTA = AnsiColor(95, 105)
    BRIGHT_CYAN = AnsiColor(96, 106)
    BRIGHT_WHITE = AnsiColor(97, 107)


class StyleKey(Enum):
    FOREGROUND = "style_key_foreground"
    BACKGROUND = "style_key_background"
    MODIFIERS = "style_key_modifiers"
