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

import pytest

from tinterm.attributes import Color, Modifier, StyleKey
from tinterm.styled import StyledString, StyledText


class TestStyledString:
    """Tests for the StyledString class."""

    def test_init_with_text_only(self):
        """Test creating a StyledString with just text."""
        s = StyledString("hello")
        assert s.text == "hello"
        assert s.style == {}

    def test_init_with_text_and_style(self):
        """Test creating a StyledString with text and style."""
        style = {StyleKey.FOREGROUND: Color.RED}
        s = StyledString("hello", style=style)
        assert s.text == "hello"
        assert s.style == style
        assert s.style[StyleKey.FOREGROUND] == Color.RED

    def test_init_with_empty_text(self):
        """Test creating a StyledString with empty text."""
        s = StyledString("")
        assert s.text == ""
        assert s.style == {}

    def test_init_with_empty_text_and_style(self):
        """Test creating a StyledString with empty text but with style."""
        style = {StyleKey.FOREGROUND: Color.BLUE}
        s = StyledString("", style=style)
        assert s.text == ""
        assert s.style == style

    def test_init_with_none_style(self):
        """Test that None style is converted to empty dict."""
        s = StyledString("hello", style=None)
        assert s.style == {}

    def test_init_with_complex_style(self):
        """Test creating a StyledString with all style options."""
        style = {
            StyleKey.FOREGROUND: Color.RED,
            StyleKey.BACKGROUND: Color.WHITE,
            StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE],
        }
        s = StyledString("hello", style=style)
        assert s.style == style
        assert s.style[StyleKey.FOREGROUND] == Color.RED
        assert s.style[StyleKey.BACKGROUND] == Color.WHITE
        assert s.style[StyleKey.MODIFIERS] == [Modifier.BOLD, Modifier.UNDERLINE]

    def test_init_style_is_immutable(self):
        """Test that modifying the original style dict doesn't affect StyledString."""
        style = {StyleKey.FOREGROUND: Color.RED}
        s = StyledString("hello", style=style)
        # Modifying the original style dict should NOT affect the StyledString
        style[StyleKey.BACKGROUND] = Color.BLUE
        assert StyleKey.BACKGROUND not in s.style
        assert len(s.style) == 1
        assert s.style[StyleKey.FOREGROUND] == Color.RED

    def test_style_property_is_immutable(self):
        """Test that attempting to modify the style dict raises TypeError."""
        style = {StyleKey.FOREGROUND: Color.RED}
        s = StyledString("hello", style=style)
        # Attempting to modify the style should raise TypeError
        with pytest.raises(TypeError):
            s.style[StyleKey.BACKGROUND] = Color.BLUE

    # style property tests
    def test_style_property_getter(self):
        """Test that style property returns a read-only view with same values."""
        style = {StyleKey.FOREGROUND: Color.GREEN}
        s = StyledString("test", style=style)
        # Should not be the same object (MappingProxyType returns a view)
        assert s.style is not style
        # But should contain the same values
        assert s.style == style
        assert s.style[StyleKey.FOREGROUND] == Color.GREEN

    # __len__ tests
    def test_len_with_text(self):
        """Test length calculation for normal text."""
        s = StyledString("hello")
        assert len(s) == 5

    def test_len_with_empty_text(self):
        """Test length of empty text."""
        s = StyledString("")
        assert len(s) == 0

    def test_len_with_unicode(self):
        """Test length calculation with unicode characters."""
        s = StyledString("hello 世界")
        assert len(s) == 8

    def test_len_with_whitespace(self):
        """Test length includes whitespace."""
        s = StyledString("hello world")
        assert len(s) == 11

    # __str__ tests
    def test_str_returns_text(self):
        """Test that str() returns the text content."""
        s = StyledString("hello")
        assert str(s) == "hello"

    def test_str_with_style(self):
        """Test that str() returns plain text even with styling."""
        style = {StyleKey.FOREGROUND: Color.RED, StyleKey.MODIFIERS: [Modifier.BOLD]}
        s = StyledString("hello", style=style)
        assert str(s) == "hello"

    def test_str_with_empty_text(self):
        """Test str() with empty text."""
        s = StyledString("")
        assert str(s) == ""

    # __add__ tests
    def test_add_two_styled_strings(self):
        """Test adding two StyledStrings creates StyledText."""
        s1 = StyledString("hello")
        s2 = StyledString("world")
        result = s1 + s2
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0] is s1
        assert result.parts[1] is s2

    def test_add_styled_string_and_plain_string(self):
        """Test adding a StyledString and a plain string."""
        s1 = StyledString("hello")
        result = s1 + " world"
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0] is s1
        assert isinstance(result.parts[1], StyledString)
        assert result.parts[1].text == " world"
        assert result.parts[1].style == {}

    def test_add_styled_string_and_number(self):
        """Test adding a StyledString and a number."""
        s1 = StyledString("Count: ")
        result = s1 + 42
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[1].text == "42"

    def test_add_styled_string_and_none(self):
        """Test adding a StyledString and None."""
        s1 = StyledString("hello")
        result = s1 + None
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[1].text == "None"

    def test_add_with_different_styles(self):
        """Test adding StyledStrings with different styles."""
        s1 = StyledString("red", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString("blue", style={StyleKey.FOREGROUND: Color.BLUE})
        result = s1 + s2
        assert isinstance(result, StyledText)
        assert result.parts[0].style[StyleKey.FOREGROUND] == Color.RED
        assert result.parts[1].style[StyleKey.FOREGROUND] == Color.BLUE

    def test_add_chaining(self):
        """Test chaining multiple additions."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        result = s1 + s2 + s3
        assert isinstance(result, StyledText)
        assert len(result.parts) == 3
        assert str(result) == "abc"

    # __radd__ tests
    def test_radd_plain_string_and_styled_string(self):
        """Test right addition with plain string."""
        s1 = StyledString("world")
        result = "hello " + s1
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0].text == "hello "
        assert result.parts[0].style == {}
        assert result.parts[1] is s1

    def test_radd_number_and_styled_string(self):
        """Test right addition with number."""
        s1 = StyledString(" items")
        result = 42 + s1
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0].text == "42"
        assert result.parts[1] is s1

    def test_radd_with_sum_builtin(self):
        """Test using sum() with StyledStrings."""
        strings = [StyledString("a"), StyledString("b"), StyledString("c")]
        # sum() uses 0 as default start, which will use __radd__
        result = sum(strings, StyledString(""))
        assert isinstance(result, StyledText)
        assert str(result) == "abc"


class TestStyledText:
    """Tests for the StyledText class."""

    # __init__ tests
    def test_init_with_empty_list(self):
        """Test creating a StyledText with empty parts list."""
        st = StyledText([])
        assert st.parts == ()
        assert isinstance(st.parts, tuple)

    def test_init_with_single_part(self):
        """Test creating a StyledText with one part."""
        s = StyledString("hello")
        st = StyledText([s])
        assert len(st.parts) == 1
        assert st.parts[0] is s
        assert isinstance(st.parts, tuple)

    def test_init_with_multiple_parts(self):
        """Test creating a StyledText with multiple parts."""
        s1 = StyledString("hello")
        s2 = StyledString("world")
        st = StyledText([s1, s2])
        assert len(st.parts) == 2
        assert st.parts[0] is s1
        assert st.parts[1] is s2
        assert isinstance(st.parts, tuple)

    def test_init_parts_are_immutable(self):
        """Test that the parts tuple cannot be modified after creation."""
        parts = [StyledString("hello")]
        st = StyledText(parts)
        # The original list can be modified
        parts.append(StyledString("world"))
        # But it should NOT affect the StyledText (stored as tuple)
        assert len(st.parts) == 1
        # Attempting to modify the tuple should raise TypeError
        with pytest.raises(TypeError):
            st.parts[0] = StyledString("modified")

    # _from_parts tests
    def test_from_parts_two_styled_strings(self):
        """Test _from_parts with two StyledStrings."""
        s1 = StyledString("hello")
        s2 = StyledString("world")
        st = StyledText._from_parts(s1, s2)
        assert len(st.parts) == 2
        assert st.parts[0] is s1
        assert st.parts[1] is s2

    def test_from_parts_styled_string_and_plain_string(self):
        """Test _from_parts with StyledString and plain string."""
        s1 = StyledString("hello")
        st = StyledText._from_parts(s1, " world")
        assert len(st.parts) == 2
        assert st.parts[0] is s1
        assert isinstance(st.parts[1], StyledString)
        assert st.parts[1].text == " world"

    def test_from_parts_plain_string_and_styled_string(self):
        """Test _from_parts with plain string first."""
        s1 = StyledString("world")
        st = StyledText._from_parts("hello ", s1)
        assert len(st.parts) == 2
        assert st.parts[0].text == "hello "
        assert st.parts[1] is s1

    def test_from_parts_with_styled_text(self):
        """Test _from_parts flattens nested StyledText."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        st1 = StyledText([s1, s2])
        st2 = StyledText._from_parts(st1, s3)
        # Should flatten st1's parts
        assert len(st2.parts) == 3
        assert st2.parts[0] is s1
        assert st2.parts[1] is s2
        assert st2.parts[2] is s3

    def test_from_parts_two_styled_texts(self):
        """Test _from_parts with two StyledText objects."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        s4 = StyledString("d")
        st1 = StyledText([s1, s2])
        st2 = StyledText([s3, s4])
        st3 = StyledText._from_parts(st1, st2)
        assert len(st3.parts) == 4
        assert st3.parts[0] is s1
        assert st3.parts[1] is s2
        assert st3.parts[2] is s3
        assert st3.parts[3] is s4

    def test_from_parts_with_numbers(self):
        """Test _from_parts converts numbers to strings."""
        st = StyledText._from_parts(42, 3.14)
        assert len(st.parts) == 2
        assert st.parts[0].text == "42"
        assert st.parts[1].text == "3.14"

    def test_from_parts_with_none(self):
        """Test _from_parts handles None."""
        st = StyledText._from_parts(None, "text")
        assert len(st.parts) == 2
        assert st.parts[0].text == "None"
        assert st.parts[1].text == "text"

    def test_from_parts_with_boolean(self):
        """Test _from_parts handles boolean values."""
        st = StyledText._from_parts(True, False)
        assert len(st.parts) == 2
        assert st.parts[0].text == "True"
        assert st.parts[1].text == "False"

    # parts property tests
    def test_parts_property(self):
        """Test that parts property returns an immutable tuple."""
        s1 = StyledString("hello")
        s2 = StyledString("world")
        st = StyledText([s1, s2])
        assert isinstance(st.parts, tuple)
        assert len(st.parts) == 2
        assert st.parts[0] is s1
        assert st.parts[1] is s2

    # __len__ tests
    def test_len_empty(self):
        """Test length of empty StyledText."""
        st = StyledText([])
        assert len(st) == 0

    def test_len_single_part(self):
        """Test length with single part."""
        st = StyledText([StyledString("hello")])
        assert len(st) == 5

    def test_len_multiple_parts(self):
        """Test length with multiple parts."""
        st = StyledText(
            [StyledString("hello"), StyledString(" "), StyledString("world")]
        )
        assert len(st) == 11

    def test_len_with_empty_parts(self):
        """Test length calculation includes empty parts."""
        st = StyledText(
            [StyledString("hello"), StyledString(""), StyledString("world")]
        )
        assert len(st) == 10

    # __iter__ tests
    def test_iter_empty(self):
        """Test iterating over empty StyledText."""
        st = StyledText([])
        result = list(st)
        assert result == []

    def test_iter_single_part(self):
        """Test iterating over single part."""
        s = StyledString("hello")
        st = StyledText([s])
        result = list(st)
        assert len(result) == 1
        assert result[0] is s

    def test_iter_multiple_parts(self):
        """Test iterating over multiple parts."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        st = StyledText([s1, s2, s3])
        result = list(st)
        assert len(result) == 3
        assert result[0] is s1
        assert result[1] is s2
        assert result[2] is s3

    def test_iter_in_for_loop(self):
        """Test using StyledText in a for loop."""
        parts = [StyledString("a"), StyledString("b"), StyledString("c")]
        st = StyledText(parts)
        collected = []
        for part in st:
            collected.append(part)
        assert collected == parts

    # __add__ tests
    def test_add_styled_text_and_styled_string(self):
        """Test adding StyledText and StyledString."""
        s1 = StyledString("hello")
        s2 = StyledString("world")
        st1 = StyledText([s1])
        result = st1 + s2
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0] is s1
        assert result.parts[1] is s2

    def test_add_styled_text_and_plain_string(self):
        """Test adding StyledText and plain string."""
        s1 = StyledString("hello")
        st1 = StyledText([s1])
        result = st1 + " world"
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[1].text == " world"

    def test_add_two_styled_texts(self):
        """Test adding two StyledText objects."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        st1 = StyledText([s1, s2])
        st2 = StyledText([s3])
        result = st1 + st2
        assert isinstance(result, StyledText)
        assert len(result.parts) == 3
        assert result.parts[0] is s1
        assert result.parts[1] is s2
        assert result.parts[2] is s3

    def test_add_chaining(self):
        """Test chaining multiple additions."""
        st1 = StyledText([StyledString("a")])
        st2 = StyledText([StyledString("b")])
        st3 = StyledText([StyledString("c")])
        result = st1 + st2 + st3
        assert len(result.parts) == 3
        assert str(result) == "abc"

    # __radd__ tests
    def test_radd_plain_string_and_styled_text(self):
        """Test right addition with plain string."""
        st = StyledText([StyledString("world")])
        result = "hello " + st
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0].text == "hello "
        assert result.parts[1].text == "world"

    def test_radd_styled_string_and_styled_text(self):
        """Test right addition with StyledString."""
        s1 = StyledString("hello")
        st = StyledText([StyledString("world")])
        result = s1 + st
        assert isinstance(result, StyledText)
        assert len(result.parts) == 2
        assert result.parts[0] is s1
        assert result.parts[1].text == "world"

    def test_radd_number_and_styled_text(self):
        """Test right addition with number."""
        st = StyledText([StyledString(" items")])
        result = 42 + st
        assert isinstance(result, StyledText)
        assert result.parts[0].text == "42"
        assert result.parts[1].text == " items"

    # __str__ tests
    def test_str_empty(self):
        """Test str() with empty StyledText."""
        st = StyledText([])
        assert str(st) == ""

    def test_str_single_part(self):
        """Test str() with single part."""
        st = StyledText([StyledString("hello")])
        assert str(st) == "hello"

    def test_str_multiple_parts(self):
        """Test str() concatenates all parts."""
        st = StyledText(
            [StyledString("hello"), StyledString(" "), StyledString("world")]
        )
        assert str(st) == "hello world"

    def test_str_ignores_styling(self):
        """Test that str() returns plain text without styling."""
        st = StyledText(
            [
                StyledString("red", style={StyleKey.FOREGROUND: Color.RED}),
                StyledString("blue", style={StyleKey.FOREGROUND: Color.BLUE}),
            ]
        )
        assert str(st) == "redblue"

    def test_str_with_empty_parts(self):
        """Test str() handles empty parts."""
        st = StyledText(
            [StyledString("hello"), StyledString(""), StyledString("world")]
        )
        assert str(st) == "helloworld"


class TestStyledStringAndTextIntegration:
    """Integration tests for StyledString and StyledText working together."""

    def test_complex_concatenation(self):
        """Test complex concatenation scenarios."""
        s1 = StyledString("Error", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString(": ", style={})
        s3 = StyledString("File not found", style={StyleKey.FOREGROUND: Color.YELLOW})

        result = s1 + s2 + s3
        assert isinstance(result, StyledText)
        assert len(result.parts) == 3
        assert str(result) == "Error: File not found"

    def test_mixed_concatenation_with_plain_strings(self):
        """Test mixing styled and plain strings."""
        s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.GREEN})
        result = "Greeting: " + s1 + " World!"

        assert isinstance(result, StyledText)
        assert len(result.parts) == 3
        assert str(result) == "Greeting: Hello World!"
        assert result.parts[0].text == "Greeting: "
        assert result.parts[1].text == "Hello"
        assert result.parts[2].text == " World!"

    def test_nested_styled_text_flattening(self):
        """Test that nested StyledText objects are properly flattened."""
        s1 = StyledString("a")
        s2 = StyledString("b")
        s3 = StyledString("c")
        s4 = StyledString("d")

        st1 = s1 + s2  # StyledText([s1, s2])
        st2 = s3 + s4  # StyledText([s3, s4])
        result = st1 + st2  # Should flatten to 4 parts

        assert len(result.parts) == 4
        assert str(result) == "abcd"

    def test_style_preservation_through_concatenation(self):
        """Test that styles are preserved when concatenating."""
        red = StyledString("RED", style={StyleKey.FOREGROUND: Color.RED})
        blue = StyledString("BLUE", style={StyleKey.FOREGROUND: Color.BLUE})
        green = StyledString("GREEN", style={StyleKey.FOREGROUND: Color.GREEN})

        result = red + " " + blue + " " + green

        assert result.parts[0].style[StyleKey.FOREGROUND] == Color.RED
        assert result.parts[1].style == {}
        assert result.parts[2].style[StyleKey.FOREGROUND] == Color.BLUE
        assert result.parts[3].style == {}
        assert result.parts[4].style[StyleKey.FOREGROUND] == Color.GREEN

    def test_empty_string_handling(self):
        """Test handling of empty strings in various scenarios."""
        s1 = StyledString("")
        s2 = StyledString("text")
        s3 = StyledString("")

        result = s1 + s2 + s3
        assert len(result.parts) == 3
        assert str(result) == "text"
        assert len(result) == 4  # Only counts "text"

    def test_length_calculation_across_types(self):
        """Test that length is calculated correctly across different types."""
        s1 = StyledString("hello")
        result1 = s1 + " world"

        assert len(s1) == 5
        assert len(result1) == 11

        result2 = result1 + "!"
        assert len(result2) == 12
