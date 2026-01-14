from tinterm.attributes import AnsiColor, Color, Modifier, StyleKey


def test_modifier_bold():
    assert Modifier.BOLD == 1


def test_modifier_dim():
    assert Modifier.DIM == 2


def test_modifier_italic():
    assert Modifier.ITALIC == 3


def test_modifier_underline():
    assert Modifier.UNDERLINE == 4


def test_modifier_blink():
    assert Modifier.BLINK == 5


def test_modifier_reverse():
    assert Modifier.REVERSE == 7


def test_modifier_strikethrough():
    assert Modifier.STRIKETHROUGH == 9


def test_color_black():
    assert Color.BLACK.value == AnsiColor(30, 40)


def test_color_red():
    assert Color.RED.value == AnsiColor(31, 41)


def test_color_green():
    assert Color.GREEN.value == AnsiColor(32, 42)


def test_color_yellow():
    assert Color.YELLOW.value == AnsiColor(33, 43)


def test_color_blue():
    assert Color.BLUE.value == AnsiColor(34, 44)


def test_color_magenta():
    assert Color.MAGENTA.value == AnsiColor(35, 45)


def test_color_cyan():
    assert Color.CYAN.value == AnsiColor(36, 46)


def test_color_white():
    assert Color.WHITE.value == AnsiColor(37, 47)


def test_color_bright_black():
    assert Color.BRIGHT_BLACK.value == AnsiColor(90, 100)


def test_color_bright_red():
    assert Color.BRIGHT_RED.value == AnsiColor(91, 101)


def test_color_bright_green():
    assert Color.BRIGHT_GREEN.value == AnsiColor(92, 102)


def test_color_bright_yellow():
    assert Color.BRIGHT_YELLOW.value == AnsiColor(93, 103)


def test_color_bright_blue():
    assert Color.BRIGHT_BLUE.value == AnsiColor(94, 104)


def test_color_bright_magenta():
    assert Color.BRIGHT_MAGENTA.value == AnsiColor(95, 105)


def test_color_bright_cyan():
    assert Color.BRIGHT_CYAN.value == AnsiColor(96, 106)


def test_color_bright_white():
    assert Color.BRIGHT_WHITE.value == AnsiColor(97, 107)


def test_stylekey_foreground():
    assert StyleKey.FOREGROUND.value == "style_key_foreground"


def test_stylekey_background():
    assert StyleKey.BACKGROUND.value == "style_key_background"


def test_stylekey_modifiers():
    assert StyleKey.MODIFIERS.value == "style_key_modifiers"
