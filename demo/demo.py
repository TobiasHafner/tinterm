from termtint.styled import StyledString, StyledText
from termtint.attributes import Color, Modifier, StyleKey
from termtint.render import render


def print_section_header(text):
    header = StyledString(text, style={
        StyleKey.FOREGROUND: Color.BRIGHT_WHITE,
        StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE]
    })
    print("\n" + render(header))
    print()


def print_color_table():
    print_section_header("FOREGROUND COLORS")
    
    standard_colors = [
        Color.BLACK, Color.RED, Color.GREEN, Color.YELLOW,
        Color.BLUE, Color.MAGENTA, Color.CYAN, Color.WHITE
    ]
    
    for color in standard_colors:
        color_name = color.name.ljust(15)
        sample_text = "Sample Text"
        
        styled = StyledString(sample_text, style={
            StyleKey.FOREGROUND: color
        })
        
        label = StyledString(color_name, style={
            StyleKey.FOREGROUND: Color.BRIGHT_BLACK
        })
        
        line = label + " " + styled
        print(render(line))
    
    print()
    
    bright_colors = [
        Color.BRIGHT_BLACK, Color.BRIGHT_RED, Color.BRIGHT_GREEN, Color.BRIGHT_YELLOW,
        Color.BRIGHT_BLUE, Color.BRIGHT_MAGENTA, Color.BRIGHT_CYAN, Color.BRIGHT_WHITE
    ]
    
    for color in bright_colors:
        color_name = color.name.ljust(15)
        sample_text = "Sample Text"
        
        styled = StyledString(sample_text, style={
            StyleKey.FOREGROUND: color
        })
        
        label = StyledString(color_name, style={
            StyleKey.FOREGROUND: Color.BRIGHT_BLACK
        })
        
        line = label + " " + styled
        print(render(line))
    
    print_section_header("BACKGROUND COLORS")
    
    all_colors = standard_colors + bright_colors
    
    for color in all_colors:
        color_name = color.name.ljust(15)
        sample_text = " Sample Text "
        
        fg_color = Color.BLACK if 'WHITE' in color.name or 'BRIGHT' in color.name else Color.WHITE
        
        styled = StyledString(sample_text, style={
            StyleKey.FOREGROUND: fg_color,
            StyleKey.BACKGROUND: color
        })
        
        label = StyledString(color_name, style={
            StyleKey.FOREGROUND: Color.BRIGHT_BLACK
        })
        
        line = label + " " + styled
        print(render(line))


def print_modifier_table():
    print_section_header("TEXT MODIFIERS")
    
    modifiers = [
        Modifier.BOLD,
        Modifier.DIM,
        Modifier.ITALIC,
        Modifier.UNDERLINE,
        Modifier.BLINK,
        Modifier.REVERSE,
        Modifier.STRIKETHROUGH
    ]
    
    for modifier in modifiers:
        modifier_name = modifier.name.ljust(15)
        sample_text = "Sample Text"
        
        styled = StyledString(sample_text, style={
            StyleKey.FOREGROUND: Color.CYAN,
            StyleKey.MODIFIERS: [modifier]
        })
        
        label = StyledString(modifier_name, style={
            StyleKey.FOREGROUND: Color.BRIGHT_BLACK
        })
        
        line = label + " " + styled
        print(render(line))


def print_combination_examples():
    print_section_header("COMBINATION EXAMPLES")
    
    error_label = StyledString("ERROR", style={
        StyleKey.FOREGROUND: Color.WHITE,
        StyleKey.BACKGROUND: Color.RED,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    error_msg = StyledString(" Connection failed", style={
        StyleKey.FOREGROUND: Color.RED
    })
    print(render(error_label + error_msg))
    
    success_label = StyledString("SUCCESS", style={
        StyleKey.FOREGROUND: Color.BLACK,
        StyleKey.BACKGROUND: Color.GREEN,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    success_msg = StyledString(" Operation completed", style={
        StyleKey.FOREGROUND: Color.GREEN
    })
    print(render(success_label + success_msg))
    
    warning_label = StyledString("WARNING", style={
        StyleKey.FOREGROUND: Color.BLACK,
        StyleKey.BACKGROUND: Color.YELLOW,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    warning_msg = StyledString(" Low disk space", style={
        StyleKey.FOREGROUND: Color.YELLOW
    })
    print(render(warning_label + warning_msg))
    
    info_label = StyledString("INFO", style={
        StyleKey.FOREGROUND: Color.WHITE,
        StyleKey.BACKGROUND: Color.BLUE,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    info_msg = StyledString(" Loading configuration...", style={
        StyleKey.FOREGROUND: Color.CYAN
    })
    print(render(info_label + info_msg))
    
    print()
    rainbow = (
        StyledString("R", style={StyleKey.FOREGROUND: Color.RED, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("A", style={StyleKey.FOREGROUND: Color.YELLOW, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("I", style={StyleKey.FOREGROUND: Color.GREEN, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("N", style={StyleKey.FOREGROUND: Color.CYAN, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("B", style={StyleKey.FOREGROUND: Color.BLUE, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("O", style={StyleKey.FOREGROUND: Color.MAGENTA, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString("W", style={StyleKey.FOREGROUND: Color.RED, StyleKey.MODIFIERS: [Modifier.BOLD]}) +
        StyledString(" Text!", style={StyleKey.FOREGROUND: Color.WHITE})
    )
    print(render(rainbow))


def main():
    title = StyledString("╔═════════════════════════════════╗", style={
        StyleKey.FOREGROUND: Color.BRIGHT_CYAN,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    title_text = StyledString("║    TermTint Demo Application    ║", style={
        StyleKey.FOREGROUND: Color.BRIGHT_CYAN,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    title_bottom = StyledString("╚═════════════════════════════════╝", style={
        StyleKey.FOREGROUND: Color.BRIGHT_CYAN,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    })
    
    print(render(title))
    print(render(title_text))
    print(render(title_bottom))
    
    print_color_table()
    print_modifier_table()
    print_combination_examples()
    
    print("\n")


if __name__ == "__main__":
    main()
