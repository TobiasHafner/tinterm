# TinTerm

A lightweight, cross-platform Python library for styling terminal output with colors and text modifiers. It provides an intuitive API for creating styled text that works consistently across Windows, macOS, and Linux by automatically handling platform differences. Further a no-color mode is provided for environments where ANSI codes aren't supported.

## Getting Started For Regular Users
Install TinTerm using pip:

```bash
pip install tinterm
```

**Note:** On Windows, the `colorama` package is automatically installed as a dependency to enable ANSI color support.

## Getting Started For Developers
If you want to build and install TinTerm from source:

### 1. Clone the repository
```bash
git clone git@github.com:TobiasHafner/tinterm.git
cd tinterm
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
In cmd:
```bash
.venv\Scripts\activate
```

In powershell:
```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install in development mode
```bash
pip install -e .
```

This installs the package in "editable" mode, so changes to the source code are immediately reflected without reinstalling.

### 5. Install development dependencies
```bash
pip install -e ".[dev]"
```

### 6. Build the package
```bash
python -m build
```

This creates distribution files in the `dist/` directory:
- `tinterm-x.x.x-py3-none-any.whl` (wheel format)
- `tinterm-x.x.x.tar.gz` (source distribution)

### 7. Install from the built package
```bash
pip install dist/tinterm-x.x.x-py3-none-any.whl
```

### 8. Run the Demo
To verify the installation and to see TinTerm's features in action, you can run the included demo application:

```bash
# From the repository root directory
python demo/demo.py
```

The demo displays:
- All 16 foreground colors (standard and bright variants)
- All background colors with contrasting text
- All 7 text modifiers (bold, dim, italic, underline, blink, reverse, strikethrough)
- Practical examples like error/success/warning messages
- Creative combinations like rainbow text

## Basic Concepts
Understanding these core concepts will help you use TinTerm effectively.

### Colors
TinTerm supports two types of colors: **foreground** (text color) and **background** (background color). Colors are defined using the `Color` enum and can be applied to text through the style dictionary.
TinTerm provides 16 colors total: 8 standard colors and 8 bright variants.

**Standard Colors:**
- `Color.BLACK` - Standard black
- `Color.RED` - Standard red
- `Color.GREEN` - Standard green
- `Color.YELLOW` - Standard yellow
- `Color.BLUE` - Standard blue
- `Color.MAGENTA` - Standard magenta
- `Color.CYAN` - Standard cyan
- `Color.WHITE` - Standard white

**Bright Colors:**
- `Color.BRIGHT_BLACK` - Bright black (gray)
- `Color.BRIGHT_RED` - Bright red
- `Color.BRIGHT_GREEN` - Bright green
- `Color.BRIGHT_YELLOW` - Bright yellow
- `Color.BRIGHT_BLUE` - Bright blue
- `Color.BRIGHT_MAGENTA` - Bright magenta
- `Color.BRIGHT_CYAN` - Bright cyan
- `Color.BRIGHT_WHITE` - Bright white

### Modifiers
Modifiers change how text appears beyond just color. They can make text bold, underlined, italic, and more. Multiple modifiers can be combined on the same text.

**Available Modifiers:**

| Modifier | Effect | ANSI Code | Terminal Support |
|----------|--------|-----------|------------------|
| `Modifier.BOLD` | Bold/bright text | 1 | Universal |
| `Modifier.DIM` | Dimmed text | 2 | Most terminals |
| `Modifier.ITALIC` | Italic text | 3 | Modern terminals |
| `Modifier.UNDERLINE` | Underlined text | 4 | Universal |
| `Modifier.BLINK` | Blinking text | 5 | Limited support |
| `Modifier.REVERSE` | Inverted foreground/background | 7 | Universal |
| `Modifier.STRIKETHROUGH` | Strikethrough text | 9 | Modern terminals |

### Styles
A style is a dictionary that defines how text should appear. It uses `StyleKey` enum values as keys and specifies colors and modifiers as values. All style keys are optional. You can specify just a foreground color, just modifiers, or any combination.

**Example:**
```python
style = {
    StyleKey.FOREGROUND: Color.RED,           # Optional: text color
    StyleKey.BACKGROUND: Color.WHITE,         # Optional: background color
    StyleKey.MODIFIERS: [Modifier.BOLD]       # Optional: text modifiers (list)
}
```

**Important Note About Modifiers:**
Modifiers should be provided as a **list** (not a tuple):

```python
# Correct
style = {StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE]}

# Also works, but list is preferred
style = {StyleKey.MODIFIERS: (Modifier.BOLD, Modifier.UNDERLINE)}
```

**Reusing Styles:**
It's good practice to define styles once and reuse them throughout your application:

```python
# Define your application's style guide
STYLES = {
    'error': {
        StyleKey.FOREGROUND: Color.RED,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    },
    'success': {
        StyleKey.FOREGROUND: Color.GREEN,
        StyleKey.MODIFIERS: [Modifier.BOLD]
    },
    'info': {
        StyleKey.FOREGROUND: Color.BLUE
    },
    'warning': {
        StyleKey.FOREGROUND: Color.YELLOW
    }
}

# Use them consistently
error_msg = StyledString("Error occurred", style=STYLES['error'])
success_msg = StyledString("Task completed", style=STYLES['success'])
```

### Styled Strings
A `StyledString` is the fundamental building block of TinTerm. It's a string with associated styling information.

**Key Characteristics:**
- **Stores text and style separately**: The text is stored in the `text` attribute, and styling in the `style` dictionary
- **Lightweight**: Uses `__slots__` for memory efficiency
- **String representation**: The `__str__()` method returns only the plain text without styling
- **Immutable styling**: Once created, the style doesn't change (but you can create new styled strings)
- **Composable**: Can be concatenated with other styled strings or plain strings/objects

**Creating Styled Strings:**
```python
# With style
my_style = {
    StyleKey.FOREGROUND: Color.RED,
    StyleKey.MODIFIERS: [Modifier.BOLD]
}
styled = StyledString("Hello", style=my_style)

# Without style (plain text)
plain = StyledString("Hello", style={})
# or simply
plain = StyledString("Hello")
```

**Accessing Properties:**
```python
s = StyledString("hello", style={StyleKey.FOREGROUND: Color.BLUE})

# Access the plain text
s.text          # "hello"
str(s)          # "hello" (same as s.text)

# Access the style dictionary
s.style         # {StyleKey.FOREGROUND: Color.BLUE}

# Get length
len(s)          # 5 (length of the text)
```

**Concatenation:**
When you concatenate `StyledString` objects, you create a `StyledText` object:

```python
red = StyledString("Red", style={StyleKey.FOREGROUND: Color.RED})
blue = StyledString("Blue", style={StyleKey.FOREGROUND: Color.BLUE})

# All of these create StyledText objects
combined1 = red + blue              # Two StyledStrings
combined2 = red + " "               # StyledString + plain string
combined3 = "Prefix: " + red        # Plain string + StyledString
```

**Notes:**
- The `StyledString` class doesn't provide string manipulation methods like `upper()`, `lower()`, `split()`, etc. You need to manipulate the text yourself and create new `StyledString` objects if needed
- Converting to string with `str()` returns only the plain text without any styling or ANSI codes
- Empty strings can have styles: `StyledString("", style={StyleKey.FOREGROUND: Color.RED})`

### Styled Text
A `StyledText` object represents multiple parts concatenated together, where each part can have its own independent styling. Each part is stored internally as a `StyledString`.

**Creating Styled Texts:**
You don't typically create `StyledText` objects directly using the constructor. They're automatically created when you concatenate `StyledString` objects or mix styled strings with plain strings/objects:

```python
part1 = StyledString("Error", style={StyleKey.FOREGROUND: Color.RED})
part2 = StyledString(": ", style={})
part3 = StyledString("Connection failed", style={StyleKey.FOREGROUND: Color.YELLOW})

# This automatically creates a StyledText with three parts
message = part1 + part2 + part3

# Mixing with plain strings also works
mixed = part1 + " " + part2  # The " " becomes a StyledString internally
```

**How StyledText._from_parts() Works:**
The `_from_parts()` static method intelligently handles different input types:
- `StyledText` objects are flattened (their parts are extracted and added individually)
- `StyledString` objects are added directly
- Other objects are converted to strings and wrapped in a `StyledString` with no styling

```python
# These all work
text1 = StyledString("Hello") + StyledString("World")
text2 = StyledString("Hello") + " World"  # String becomes StyledString
text3 = StyledString("Count: ") + 42       # Number becomes StyledString("42")
```

**Structure:**
A `StyledText` maintains a list of `StyledString` parts accessible via the `parts` property:

```python
# Accessing parts
for part in message.parts:
    print(f"Text: {part.text}, Style: {part.style}")
```

**Operations:**
`StyledText` supports several operations:

```python
text = red_string + " " + blue_string + " " + green_string

# Concatenation (returns new StyledText)
more_text = text + StyledString(" More", style={StyleKey.FOREGROUND: Color.YELLOW})
more_text = text + " More"  # Also works

# Length (total length of all parts)
len(text)

# Iteration over parts
for part in text:
    print(render(part))

# String representation (plain text only, no styling)
str(text)  # Concatenated plain text from all parts
```

**Why StyledText Matters:**
`StyledText` allows you to build complex, multi-colored output while keeping each part's styling independent:

```python
# Build a colorful log message
timestamp = StyledString("[2024-01-12 10:30:15]", style={
    StyleKey.FOREGROUND: Color.BRIGHT_BLACK
})

level = StyledString(" ERROR ", style={
    StyleKey.FOREGROUND: Color.WHITE,
    StyleKey.BACKGROUND: Color.RED,
    StyleKey.MODIFIERS: [Modifier.BOLD]
})

message = StyledString(" Database connection failed", style={
    StyleKey.FOREGROUND: Color.RED
})

log_line = timestamp + level + message
print(render(log_line))
```

### The Render Function

The `render()` function converts your styled objects (`StyledString` or `StyledText`) into a string with ANSI escape codes that can be printed to the terminal.

**Usage:**
```python
from tinterm.render import render

styled = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
output = render(styled)
print(output)  # Prints "Hello" in red
```

**How It Works:**
The render function processes styled objects using a stack-based approach:
- For `StyledText` objects, it processes each part individually
- For `StyledString` objects, it extracts color and modifier information from the style dictionary and generates appropriate ANSI codes
- ANSI codes are wrapped around the text: `\033[<codes>m<text>\033[0m`

**Color Control:**
You can globally enable or disable color rendering:

```python
from tinterm.render import enable_colors, disable_colors

# Disable colors (returns plain text without ANSI codes)
disable_colors()
print(render(styled))  # Prints plain "Hello" without colors

# Re-enable colors
enable_colors()
print(render(styled))  # Prints "Hello" in red again
```

When colors are disabled, `render()` returns only the plain text content, which is useful for:
- Logging to files
- Running in environments without ANSI support
- Testing
- Piping output to other programs

**Performance:**
Rendering is lightweight, but if you're rendering the same styled text repeatedly in a loop, consider rendering once and reusing the result:

```python
# Less efficient
for i in range(1000):
    print(render(styled_text))

# More efficient
rendered = render(styled_text)
for i in range(1000):
    print(rendered)
```

## Complete Example

Here's a complete example showing how to use TinTerm:

```python
from tinterm.styled import StyledString, StyledText
from tinterm.attributes import Color, Modifier, StyleKey
from tinterm.render import render

# Define some styles
error_style = {
    StyleKey.FOREGROUND: Color.RED,
    StyleKey.MODIFIERS: [Modifier.BOLD]
}

success_style = {
    StyleKey.FOREGROUND: Color.GREEN,
    StyleKey.MODIFIERS: [Modifier.BOLD]
}

info_style = {
    StyleKey.FOREGROUND: Color.CYAN
}

# Create styled strings
header = StyledString("=== System Status ===", style={
    StyleKey.FOREGROUND: Color.BRIGHT_WHITE,
    StyleKey.MODIFIERS: [Modifier.BOLD, Modifier.UNDERLINE]
})

error_msg = StyledString("ERROR: ", style=error_style) + "Database connection failed"
success_msg = StyledString("SUCCESS: ", style=success_style) + "Server started on port 8080"
info_msg = StyledString("INFO: ", style=info_style) + "Loading configuration..."

# Render and print
print(render(header))
print(render(error_msg))
print(render(success_msg))
print(render(info_msg))
```
