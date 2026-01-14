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

from tinterm.attributes import Color, Modifier, StyleKey
from tinterm.render import _render_no_color, disable_colors, enable_colors, render
from tinterm.styled import StyledString, StyledText


class TestEnableDisableColors:
    """Tests for enable_colors() and disable_colors() functions."""

    def setup_method(self):
        """Ensure colors are enabled before each test."""
        enable_colors()

    def test_colors_enabled_by_default(self):
        """Test that colors are enabled by default."""
        # Create a styled string with color
        s = StyledString("test", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        # Should contain ANSI codes
        assert "\033[" in result
        assert result != "test"

    def test_disable_colors(self):
        """Test that disable_colors() disables ANSI code generation."""
        disable_colors()
        s = StyledString("test", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        # Should return plain text without ANSI codes
        assert result == "test"
        assert "\033[" not in result

    def test_enable_colors(self):
        """Test that enable_colors() re-enables ANSI code generation."""
        disable_colors()
        enable_colors()
        s = StyledString("test", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        # Should contain ANSI codes again
        assert "\033[" in result
        assert result != "test"

    def test_toggle_colors_multiple_times(self):
        """Test toggling colors on and off multiple times."""
        s = StyledString("test", style={StyleKey.FOREGROUND: Color.BLUE})

        # Start enabled
        result1 = render(s)
        assert "\033[" in result1

        # Disable
        disable_colors()
        result2 = render(s)
        assert result2 == "test"

        # Enable
        enable_colors()
        result3 = render(s)
        assert "\033[" in result3

        # Disable again
        disable_colors()
        result4 = render(s)
        assert result4 == "test"

    def teardown_method(self):
        """Re-enable colors after each test."""
        enable_colors()


class TestRenderNoColor:
    """Tests for the _render_no_color() internal function."""

    def test_render_no_color_styled_string(self):
        """Test _render_no_color with StyledString."""
        s = StyledString("hello", style={StyleKey.FOREGROUND: Color.RED})
        result = _render_no_color(s)
        assert result == "hello"

    def test_render_no_color_styled_string_no_style(self):
        """Test _render_no_color with unstyled StyledString."""
        s = StyledString("hello")
        result = _render_no_color(s)
        assert result == "hello"

    def test_render_no_color_styled_text(self):
        """Test _render_no_color with StyledText."""
        s1 = StyledString("hello", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString(" world", style={StyleKey.FOREGROUND: Color.BLUE})
        st = StyledText([s1, s2])
        result = _render_no_color(st)
        assert result == "hello world"

    def test_render_no_color_empty_styled_string(self):
        """Test _render_no_color with empty StyledString."""
        s = StyledString("")
        result = _render_no_color(s)
        assert result == ""

    def test_render_no_color_empty_styled_text(self):
        """Test _render_no_color with empty StyledText."""
        st = StyledText([])
        result = _render_no_color(st)
        assert result == ""

    def test_render_no_color_complex_styled_text(self):
        """Test _render_no_color with complex StyledText."""
        parts = [
            StyledString("Error", style={StyleKey.FOREGROUND: Color.RED}),
            StyledString(": ", style={}),
            StyledString("File not found", style={StyleKey.FOREGROUND: Color.YELLOW}),
        ]
        st = StyledText(parts)
        result = _render_no_color(st)
        assert result == "Error: File not found"


class TestRenderStyledString:
    """Tests for rendering StyledString objects."""

    def setup_method(self):
        """Ensure colors are enabled before each test."""
        enable_colors()

    def test_render_unstyled_string(self):
        """Test rendering a StyledString with no style."""
        s = StyledString("hello")
        result = render(s)
        assert result == "hello"

    def test_render_with_foreground_color(self):
        """Test rendering with foreground color."""
        s = StyledString("hello", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        assert result == "\033[31mhello\033[0m"

    def test_render_with_background_color(self):
        """Test rendering with background color."""
        s = StyledString("hello", style={StyleKey.BACKGROUND: Color.BLUE})
        result = render(s)
        assert result == "\033[44mhello\033[0m"

    def test_render_with_foreground_and_background(self):
        """Test rendering with both foreground and background colors."""
        s = StyledString(
            "hello",
            style={StyleKey.FOREGROUND: Color.RED, StyleKey.BACKGROUND: Color.WHITE},
        )
        result = render(s)
        # Should contain both color codes
        assert "\033[" in result
        assert "31" in result  # Red foreground
        assert "47" in result  # White background
        assert "hello" in result
        assert result.endswith("\033[0m")

    def test_render_with_single_modifier(self):
        """Test rendering with a single modifier."""
        s = StyledString("hello", style={StyleKey.MODIFIERS: [Modifier.BOLD]})
        result = render(s)
        assert result == "\033[1mhello\033[0m"

    def test_render_with_multiple_modifiers(self):
        """Test rendering with multiple modifiers."""
        s = StyledString(
            "hello", style={StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE]}
        )
        result = render(s)
        assert "\033[" in result
        assert "1" in result  # Bold
        assert "4" in result  # Underline
        assert "hello" in result
        assert result.endswith("\033[0m")

    def test_render_with_color_and_modifiers(self):
        """Test rendering with color and modifiers combined."""
        s = StyledString(
            "hello",
            style={
                StyleKey.FOREGROUND: Color.GREEN,
                StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.ITALIC],
            },
        )
        result = render(s)
        assert "\033[" in result
        assert "32" in result  # Green foreground
        assert "1" in result  # Bold
        assert "3" in result  # Italic
        assert "hello" in result
        assert result.endswith("\033[0m")

    def test_render_with_all_style_options(self):
        """Test rendering with all style options."""
        s = StyledString(
            "hello",
            style={
                StyleKey.FOREGROUND: Color.YELLOW,
                StyleKey.BACKGROUND: Color.BLUE,
                StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE],
            },
        )
        result = render(s)
        assert "\033[" in result
        assert "33" in result  # Yellow foreground
        assert "44" in result  # Blue background
        assert "1" in result  # Bold
        assert "4" in result  # Underline
        assert "hello" in result
        assert result.endswith("\033[0m")

    def test_render_empty_string(self):
        """Test rendering an empty StyledString."""
        s = StyledString("")
        result = render(s)
        assert result == ""

    def test_render_empty_string_with_style(self):
        """Test rendering an empty StyledString with style."""
        s = StyledString("", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        # Empty string with style should produce ANSI codes
        assert result == "\033[31m\033[0m"

    def test_render_bright_colors(self):
        """Test rendering bright color variants."""
        s = StyledString("hello", style={StyleKey.FOREGROUND: Color.BRIGHT_RED})
        result = render(s)
        assert result == "\033[91mhello\033[0m"

    def test_render_all_standard_colors(self):
        """Test rendering all standard colors."""
        colors = [
            (Color.BLACK, "30"),
            (Color.RED, "31"),
            (Color.GREEN, "32"),
            (Color.YELLOW, "33"),
            (Color.BLUE, "34"),
            (Color.MAGENTA, "35"),
            (Color.CYAN, "36"),
            (Color.WHITE, "37"),
        ]

        for color, code in colors:
            s = StyledString("test", style={StyleKey.FOREGROUND: color})
            result = render(s)
            assert f"\033[{code}m" in result

    def test_render_all_bright_colors(self):
        """Test rendering all bright colors."""
        colors = [
            (Color.BRIGHT_BLACK, "90"),
            (Color.BRIGHT_RED, "91"),
            (Color.BRIGHT_GREEN, "92"),
            (Color.BRIGHT_YELLOW, "93"),
            (Color.BRIGHT_BLUE, "94"),
            (Color.BRIGHT_MAGENTA, "95"),
            (Color.BRIGHT_CYAN, "96"),
            (Color.BRIGHT_WHITE, "97"),
        ]

        for color, code in colors:
            s = StyledString("test", style={StyleKey.FOREGROUND: color})
            result = render(s)
            assert f"\033[{code}m" in result

    def test_render_all_modifiers(self):
        """Test rendering all modifiers."""
        modifiers = [
            (Modifier.BOLD, "1"),
            (Modifier.DIM, "2"),
            (Modifier.ITALIC, "3"),
            (Modifier.UNDERLINE, "4"),
            (Modifier.BLINK, "5"),
            (Modifier.REVERSE, "7"),
            (Modifier.STRIKETHROUGH, "9"),
        ]

        for modifier, code in modifiers:
            s = StyledString("test", style={StyleKey.MODIFIERS: [modifier]})
            result = render(s)
            assert f"\033[{code}m" in result


class TestRenderStyledText:
    """Tests for rendering StyledText objects."""

    def setup_method(self):
        """Ensure colors are enabled before each test."""
        enable_colors()

    def test_render_empty_styled_text(self):
        """Test rendering empty StyledText."""
        st = StyledText([])
        result = render(st)
        assert result == ""

    def test_render_single_part(self):
        """Test rendering StyledText with single part."""
        s = StyledString("hello", style={StyleKey.FOREGROUND: Color.RED})
        st = StyledText([s])
        result = render(st)
        assert result == "\033[31mhello\033[0m"

    def test_render_multiple_parts_same_style(self):
        """Test rendering StyledText with multiple parts having same style."""
        s1 = StyledString("hello", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString(" world", style={StyleKey.FOREGROUND: Color.RED})
        st = StyledText([s1, s2])
        result = render(st)
        assert result == "\033[31mhello\033[0m\033[31m world\033[0m"

    def test_render_multiple_parts_different_styles(self):
        """Test rendering StyledText with different styles."""
        s1 = StyledString("red", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString(" blue", style={StyleKey.FOREGROUND: Color.BLUE})
        st = StyledText([s1, s2])
        result = render(st)
        assert "\033[31mred\033[0m" in result
        assert "\033[34m blue\033[0m" in result

    def test_render_mixed_styled_and_unstyled(self):
        """Test rendering StyledText with mixed styled and unstyled parts."""
        s1 = StyledString("styled", style={StyleKey.FOREGROUND: Color.GREEN})
        s2 = StyledString(" plain")
        s3 = StyledString(" styled", style={StyleKey.FOREGROUND: Color.YELLOW})
        st = StyledText([s1, s2, s3])
        result = render(st)
        assert "\033[32mstyled\033[0m" in result
        assert " plain" in result
        assert "\033[33m styled\033[0m" in result

    def test_render_complex_log_message(self):
        """Test rendering a complex log message."""
        timestamp = StyledString(
            "[2024-01-12 10:30:15]", style={StyleKey.FOREGROUND: Color.BRIGHT_BLACK}
        )
        level = StyledString(
            " ERROR ",
            style={
                StyleKey.FOREGROUND: Color.WHITE,
                StyleKey.BACKGROUND: Color.RED,
                StyleKey.MODIFIERS: [Modifier.BOLD],
            },
        )
        message = StyledString(
            " Connection failed", style={StyleKey.FOREGROUND: Color.RED}
        )
        st = StyledText([timestamp, level, message])
        result = render(st)

        # Should contain all three parts with their respective styling
        assert "\033[90m[2024-01-12 10:30:15]\033[0m" in result
        assert "37" in result  # White foreground
        assert "41" in result  # Red background
        assert "1" in result  # Bold
        assert "\033[31m Connection failed\033[0m" in result

    def test_render_concatenated_strings(self):
        """Test rendering StyledText created through concatenation."""
        s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.GREEN})
        s2 = StyledString(" ", style={})
        s3 = StyledString("World", style={StyleKey.FOREGROUND: Color.BLUE})
        st = s1 + s2 + s3
        result = render(st)

        assert "\033[32mHello\033[0m" in result
        assert " " in result
        assert "\033[34mWorld\033[0m" in result


class TestRenderEdgeCases:
    """Tests for edge cases and special scenarios."""

    def setup_method(self):
        """Ensure colors are enabled before each test."""
        enable_colors()

    def test_render_with_special_characters(self):
        """Test rendering with special characters."""
        s = StyledString("hello\nworld\ttab", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        assert "\033[31mhello\nworld\ttab\033[0m" == result

    def test_render_with_unicode(self):
        """Test rendering with unicode characters."""
        s = StyledString("Hello 世界 🌍", style={StyleKey.FOREGROUND: Color.BLUE})
        result = render(s)
        assert "\033[34mHello 世界 🌍\033[0m" == result

    def test_render_with_empty_modifier_list(self):
        """Test rendering with empty modifier list."""
        s = StyledString("hello", style={StyleKey.MODIFIERS: []})
        result = render(s)
        assert result == "hello"

    def test_render_with_none_values_in_style(self):
        """Test rendering handles None values in style gracefully."""
        # This tests the extractor functions return None for invalid values
        s = StyledString("hello", style={StyleKey.FOREGROUND: None})
        result = render(s)
        # Should render as plain text since None is not a Color
        assert result == "hello"

    def test_render_preserves_whitespace(self):
        """Test that rendering preserves whitespace."""
        s = StyledString("  hello  world  ", style={StyleKey.FOREGROUND: Color.RED})
        result = render(s)
        assert result == "\033[31m  hello  world  \033[0m"

    def test_render_very_long_text(self):
        """Test rendering very long text."""
        long_text = "a" * 10000
        s = StyledString(long_text, style={StyleKey.FOREGROUND: Color.GREEN})
        result = render(s)
        assert result.startswith("\033[32m")
        assert result.endswith("\033[0m")
        assert long_text in result

    def test_render_with_multiple_modifiers_order(self):
        """Test that modifier order doesn't matter for the result."""
        s1 = StyledString(
            "test", style={StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE]}
        )
        s2 = StyledString(
            "test", style={StyleKey.MODIFIERS: [Modifier.UNDERLINE, Modifier.BOLD]}
        )
        result1 = render(s1)
        result2 = render(s2)

        # Both should contain both modifiers
        assert "1" in result1 and "4" in result1
        assert "1" in result2 and "4" in result2

    def test_render_disabled_then_enabled_within_test(self):
        """Test disabling and enabling colors within a single test."""
        s = StyledString("test", style={StyleKey.FOREGROUND: Color.RED})

        # Render with colors
        result1 = render(s)
        assert "\033[" in result1

        # Disable and render
        disable_colors()
        result2 = render(s)
        assert result2 == "test"

        # Re-enable and render
        enable_colors()
        result3 = render(s)
        assert "\033[" in result3
        assert result3 == result1

    def teardown_method(self):
        """Re-enable colors after each test."""
        enable_colors()


class TestRenderIntegration:
    """Integration tests combining multiple features."""

    def setup_method(self):
        """Ensure colors are enabled before each test."""
        enable_colors()

    def test_render_nested_concatenation(self):
        """Test rendering deeply nested concatenated StyledText."""
        s1 = StyledString("a", style={StyleKey.FOREGROUND: Color.RED})
        s2 = StyledString("b", style={StyleKey.FOREGROUND: Color.GREEN})
        st1 = s1 + s2

        s3 = StyledString("c", style={StyleKey.FOREGROUND: Color.BLUE})
        s4 = StyledString("d", style={StyleKey.FOREGROUND: Color.YELLOW})
        st2 = s3 + s4

        st3 = st1 + st2
        result = render(st3)

        # Should contain all four colors
        assert "31" in result  # Red
        assert "32" in result  # Green
        assert "34" in result  # Blue
        assert "33" in result  # Yellow

    def test_render_with_all_features_combined(self):
        """Test rendering with all features combined."""
        parts = []

        # Add various styled parts
        parts.append(
            StyledString(
                "Bold Red ",
                style={
                    StyleKey.FOREGROUND: Color.RED,
                    StyleKey.MODIFIERS: [Modifier.BOLD],
                },
            )
        )

        parts.append(
            StyledString(
                "Italic Blue ",
                style={
                    StyleKey.FOREGROUND: Color.BLUE,
                    StyleKey.MODIFIERS: [Modifier.ITALIC],
                },
            )
        )

        parts.append(
            StyledString(
                "Underline Green ",
                style={
                    StyleKey.FOREGROUND: Color.GREEN,
                    StyleKey.MODIFIERS: [Modifier.UNDERLINE],
                },
            )
        )

        parts.append(StyledString("Plain ", style={}))

        parts.append(
            StyledString("BG Yellow", style={StyleKey.BACKGROUND: Color.YELLOW})
        )

        st = StyledText(parts)
        result = render(st)

        # Verify all styles are present
        assert "31" in result  # Red
        assert "1" in result  # Bold
        assert "34" in result  # Blue
        assert "3" in result  # Italic
        assert "32" in result  # Green
        assert "4" in result  # Underline
        assert "43" in result  # Yellow background
        assert "Plain" in result

    def test_render_realistic_cli_output(self):
        """Test rendering realistic CLI output scenario."""
        # Simulate a realistic command-line tool output
        header = StyledString(
            "MyApp v1.0.0",
            style={
                StyleKey.FOREGROUND: Color.BRIGHT_CYAN,
                StyleKey.MODIFIERS: [Modifier.BOLD],
            },
        )

        success_prefix = StyledString(
            "✓ ", style={StyleKey.FOREGROUND: Color.BRIGHT_GREEN}
        )
        success_msg = StyledString("Build completed successfully")

        warning_prefix = StyledString(
            "⚠ ", style={StyleKey.FOREGROUND: Color.BRIGHT_YELLOW}
        )
        warning_msg = StyledString("3 warnings found")

        error_prefix = StyledString(
            "✗ ",
            style={
                StyleKey.FOREGROUND: Color.BRIGHT_RED,
                StyleKey.MODIFIERS: [Modifier.BOLD],
            },
        )
        error_msg = StyledString(
            "File not found: config.json", style={StyleKey.FOREGROUND: Color.RED}
        )

        # Combine all parts
        output = (
            header
            + StyledString("\n\n")
            + success_prefix
            + success_msg
            + StyledString("\n")
            + warning_prefix
            + warning_msg
            + StyledString("\n")
            + error_prefix
            + error_msg
        )

        result = render(output)

        # Verify structure is maintained
        assert "MyApp v1.0.0" in result
        assert "✓" in result
        assert "Build completed successfully" in result
        assert "⚠" in result
        assert "3 warnings found" in result
        assert "✗" in result
        assert "File not found: config.json" in result

        # Verify colors are present
        assert "\033[" in result
        assert "\033[0m" in result

    def teardown_method(self):
        """Re-enable colors after each test."""
        enable_colors()
