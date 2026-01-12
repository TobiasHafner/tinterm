import pytest
from termtint.styled import StyledString, StyledText
from termtint.attributes import Color, Modifier, StyleKey

def test_create_styled_string_no_style():
    s = StyledString("Hello")
    assert isinstance(s, StyledString)
    assert str(s) == "Hello"
    assert s.style == {}

def test_create_styled_string_with_style():
    style = {StyleKey.FOREGROUND: Color.RED, StyleKey.MODIFIERS: (Modifier.BOLD,)}
    s = StyledString("Hi", style=style)
    assert s.style[StyleKey.FOREGROUND] == Color.RED
    assert s.style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_string_concat_left():
    s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    combined = "Start " + s1
    assert isinstance(combined, StyledText)
    assert str(combined.parts[0]) == "Start "
    assert combined.parts[0].style == {}
    assert str(combined.parts[1]) == "Hello"
    assert combined.parts[1].style[StyleKey.FOREGROUND] == Color.RED

def test_styled_string_concat_right():
    s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    combined = s1 + " End"
    assert isinstance(combined, StyledText)
    assert str(combined.parts[0]) == "Hello"
    assert combined.parts[0].style[StyleKey.FOREGROUND] == Color.RED
    assert str(combined.parts[1]) == " End"
    assert combined.parts[1].style == {}

def test_styles_string_single_character_slice():
    s = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    c = s[1]
    assert isinstance(c, StyledString)
    assert str(c) == "e"
    assert c.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_multi_character_slice():
    s = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    sub = s[1:4]
    assert isinstance(sub, StyledString)
    assert str(sub) == "ell"
    assert sub.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_upper():
    s = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    u = s.upper()
    assert isinstance(u, StyledString)
    assert str(u) == "HELLO"
    assert u.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_lower():
    s = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    l = s.lower()
    assert isinstance(l, StyledString)
    assert str(l) == "hello"
    assert l.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_title():
    s = StyledString("hello world", style={StyleKey.FOREGROUND: Color.RED})
    t = s.title()
    assert isinstance(t, StyledString)
    assert str(t) == "Hello World"
    assert t.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_capitalize():
    s = StyledString("hello world", style={StyleKey.FOREGROUND: Color.RED})
    c = s.capitalize()
    assert isinstance(c, StyledString)
    assert str(c) == "Hello world"
    assert c.style[StyleKey.FOREGROUND] == Color.RED

def test_styles_string_len():
    s = StyledString("Hello")
    assert len(s) == 5

def test_styled_text_iter():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + " " + s2
    chars = list(t)
    assert all(isinstance(c, StyledString) for c in chars)
    assert chars[0].style[StyleKey.FOREGROUND] == Color.RED
    assert chars[-1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_concat_left():
    s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("World", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = "Start " + (s1 + " " + s2)
    assert isinstance(t, StyledText)
    assert str(t.parts[1]) == "Hello"
    assert t.parts[1].style[StyleKey.FOREGROUND] == Color.RED
    assert str(t.parts[-1]) == "World"
    assert t.parts[-1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_concat_right():
    s1 = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("World", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = (s1 + " " + s2) + " End"
    assert isinstance(t, StyledText)
    assert str(t.parts[-1]) == " End"
    assert t.parts[-1].style == {}

def test_styled_text_single_character_slice():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    c = t[1]
    assert isinstance(c, StyledString)
    assert str(c) == "i"
    assert c.style[StyleKey.FOREGROUND] == Color.RED

def test_styled_text_multi_character_slice():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    sub = t[1:5]
    assert isinstance(sub, StyledText)
    assert "".join(str(p) for p in sub.parts) == "iThe"
    assert sub.parts[0].style[StyleKey.FOREGROUND] == Color.RED
    assert sub.parts[-1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_upper():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    u = t.upper()
    assert isinstance(u, StyledText)
    assert "".join(str(p) for p in u.parts) == "HITHERE"
    assert u.parts[0].style[StyleKey.FOREGROUND] == Color.RED
    assert u.parts[1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_lower():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    l = t.lower()
    assert isinstance(l, StyledText)
    assert "".join(str(p) for p in l.parts) == "hithere"
    assert l.parts[0].style[StyleKey.FOREGROUND] == Color.RED
    assert l.parts[1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_capitalize():
    s1 = StyledString("hello ", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("world", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    c = t.capitalize()
    assert isinstance(c, StyledText)
    assert "".join(str(p) for p in c.parts) == "Hello world"
    assert c.parts[0].style[StyleKey.FOREGROUND] == Color.RED
    assert c.parts[1].style[StyleKey.MODIFIERS] == (Modifier.BOLD,)

def test_styled_text_len():
    s1 = StyledString("Hi", style={StyleKey.FOREGROUND: Color.RED})
    s2 = StyledString("There", style={StyleKey.MODIFIERS: (Modifier.BOLD,)})
    t = s1 + s2
    assert len(t) == 7
