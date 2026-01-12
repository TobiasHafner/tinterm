import pytest
from termtint.styled import StyledString, StyledText
from termtint.attributes import Color, Modifier, StyleKey
from termtint.render import render, enable_colors, disable_colors

# Helper to get expected ansi codes
def ansi_code(fg=None, bg=None, modifiers=None):
    """Return expected ANSI code string given fg, bg, modifiers"""
    codes = []
    if fg is not None:
        codes.append(str(fg.value.foreground))
    if bg is not None:
        codes.append(str(bg.value.background))
    if modifiers:
        codes.extend(str(m.value) for m in modifiers)
    if not codes:
        return ""
    return f"\033[{';'.join(codes)}m"
    
def test_render_no_color_mode_plain_text():
    disable_colors()
    s = StyledString("Test")
    assert render(s) == "Test"

def test_render_no_color_mode_styled_text():
    disable_colors()
    s = StyledString("Test", style={StyleKey.FOREGROUND: Color.RED, StyleKey.MODIFIERS: (Modifier.BOLD,)})
    assert render(s) == "Test"

@pytest.mark.parametrize("fg_color", list(Color))
@pytest.mark.parametrize("bg_color", list(Color) + [None])
@pytest.mark.parametrize("modifier", list(Modifier) + [None])

def test_render_styled_string_combinations(fg_color, bg_color, modifier):
    enable_colors()
    
    style = {}
    if fg_color:
        style[StyleKey.FOREGROUND] = fg_color
    if bg_color:
        style[StyleKey.BACKGROUND] = bg_color
    if modifier:
        style[StyleKey.MODIFIERS] = (modifier,)
    
    s = StyledString("X", style=style)
    
    rendered = render(s)
    expected = ansi_code(fg_color, bg_color, (modifier,) if modifier else None)
    if expected:
        assert rendered.startswith(expected)
        assert rendered.endswith("\033[0m")
        assert "X" in rendered
    else:
        assert rendered == "X"

def test_render_styled_text_multiple_parts_various_styles():
    enable_colors()
    part1 = StyledString("R", style={StyleKey.FOREGROUND: Color.RED})
    part2 = StyledString("G", style={StyleKey.FOREGROUND: Color.GREEN, StyleKey.MODIFIERS: (Modifier.BOLD,)})
    part3 = StyledString("B", style={StyleKey.FOREGROUND: Color.BLUE, StyleKey.MODIFIERS: (Modifier.UNDERLINE,)})
    
    text = StyledText([part1, part2, part3])
    rendered = render(text)
    
    assert f"\033[31mR\033[0m" in rendered
    assert f"\033[32;1mG\033[0m" in rendered
    assert f"\033[34;4mB\033[0m" in rendered

def test_render_styled_text_no_color_mode_multiple_parts():
    disable_colors()
    part1 = StyledString("A", style={StyleKey.FOREGROUND: Color.RED})
    part2 = StyledString("B", style={StyleKey.FOREGROUND: Color.GREEN})
    text = StyledText([part1, part2])
    rendered = render(text)
    assert rendered == "AB"

