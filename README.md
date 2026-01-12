# TermTint

A lightweight, cross-platform Python library for styling terminal output with colors and text modifiers. TermTint makes it easy to add colors and styling to your terminal applications. It provides an intuitive API for creating styled text that works consistently across Windows, macOS, and Linux. The library automatically handles platform differences and includes a no-color mode for environments where ANSI codes aren't supported.

## Getting Started For Regular Users
Install TermTint using pip:

```bash
pip install termtint
```

**Note:** On Windows, the `colorama` package is automatically installed as a dependency to enable ANSI color support.

## Getting Started For Developers
If you want to build and install TermTint from source:

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/termtint.git
cd termtint
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install in development mode
```bash
pip install -e .
```

This installs the package in "editable" mode, so changes to the source code are immediately reflected without reinstalling.

### 4. Install development dependencies
```bash
pip install -e ".[dev]"
```

### 5. Build the package
```bash
python -m build
```

This creates distribution files in the `dist/` directory:
- `termtint-x.x.x-py3-none-any.whl` (wheel format)
- `termtint-x.x.x.tar.gz` (source distribution)

### 6. Install from the built package
```bash
pip install dist/termtint-x.x.x-py3-none-any.whl
```

## Basic Concepts
Understanding these core concepts will help you use TermTint effectively.

### Colors
TermTint supports two types of colors: **foreground** (text color) and **background** (background color). Colors are defined using the `Color` enum and can be applied to text through the style dictionary.
TermTint provides 16 colors total: 8 standard colors and 8 bright variants.

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
    StyleKey.MODIFIERS: (Modifier.BOLD,)      # Optional: text modifiers
}
```

**Reusing Styles:**
It's good practice to define styles once and reuse them throughout your application:

```python
# Define your application's style guide
STYLES = {
    'error': {
        StyleKey.FOREGROUND: Color.RED,
        StyleKey.MODIFIERS: (Modifier.BOLD,)
    },
    'success': {
        StyleKey.FOREGROUND: Color.GREEN,
        StyleKey.MODIFIERS: (Modifier.BOLD,)
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
A `StyledString` is the fundamental building block of TermTint. It's a string that carries styling information along with its text content.

**Key Characteristics:**
- **Behaves like a regular Python string**: You can use all standard string methods
- **Preserves styling**: Operations like `upper()`, `lower()`, or slicing maintain the style
- **Immutable styling**: Once created, the style doesn't change (but you can create new styled strings)
- **Composable**: Can be concatenated with other styled strings

**Creating Styled Strings:**
```python
# With style
my_style = {
    StyleKey.FOREGROUND: Color.RED,
    StyleKey.MODIFIERS: (Modifier.BOLD,)
}
styled = StyledString("Hello",style=my_style})

# Without style (plain text)
plain = StyledString("Hello", style={})
# or simply
plain = StyledString("Hello")
```

**String Operations:**
`StyledString` supports all operations you'd expect from a regular string:

```python
s = StyledString("hello world", style={StyleKey.FOREGROUND: Color.BLUE})

# Case transformations
s.upper()          # StyledString("HELLO WORLD") with same style
s.lower()          # StyledString("hello world") with same style
s.capitalize()     # StyledString("Hello world") with same style
s.title()          # StyledString("Hello World") with same style

# Slicing
s[0:5]             # StyledString("hello") with same style
s[6:]              # StyledString("world") with same style
s[-5:]             # StyledString("world") with same style

# String methods
s.strip()          # Removes whitespace, preserves style
s.replace("world", "Python")  # StyledString("hello Python") with same style
s.split()          # Returns list of StyledString objects

# Checking content
len(s)             # 11
"hello" in s       # True
s.startswith("hello")  # True
```

**Concatenation:**
When you concatenate `StyledString` objects with different styles, you create a `StyledText` object introduced in the next section:

```python
red = StyledString("Red", style={StyleKey.FOREGROUND: Color.RED})
blue = StyledString("Blue", style={StyleKey.FOREGROUND: Color.BLUE})

# This creates a StyledText with two parts
combined = red + " " + blue
```

**Notes:**
- Styling is preserved through transformations, but the style itself is immutable
- When you modify a `StyledString`, you get a new `StyledString` with the same style
- Empty strings can have styles: `StyledString("", style={StyleKey.FOREGROUND: Color.RED})`

### Styled Text
A `StyledText` object represents multiple `StyledString` objects concatenated together, where each part can have its own independent styling.

**Creating Styled Texts:**
You don't typically create `StyledText` objects directly. They're automatically created when you concatenate `StyledString` objects:

```python
part1 = StyledString("Error", style={StyleKey.FOREGROUND: Color.RED})
part2 = StyledString(": ", style={})
part3 = StyledString("Connection failed", style={StyleKey.FOREGROUND: Color.YELLOW})

# This automatically creates a StyledText with three parts
message = part1 + part2 + part3
```

**Structure:**
A `StyledText` maintains a list of `StyledString` parts:

```python
# Accessing parts
for part in message.parts:
    print(f"Text: {part}, Style: {part.style}")
```

**Operations:**
Like `StyledString`, `StyledText` supports many string-like operations:

```python
text = red_string + " " + blue_string + " " + green_string

# Concatenation
more_text = text + StyledString(" More", style={StyleKey.FOREGROUND: Color.YELLOW})

# Slicing (returns a new StyledText)
text[0:10]

# Length
len(text)

# Iteration
for part in text.parts:
    print(render(part))
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
    StyleKey.MODIFIERS: (Modifier.BOLD,)
})

message = StyledString(" Database connection failed", style={
    StyleKey.FOREGROUND: Color.RED
})

log_line = timestamp + level + message
print(render(log_line))
```

### The Render Function

The `render()` function is what converts your styled objects (`StyledString` or `StyledText`) into a regular python string ANSI escape codes. This regular string can then be printed to the console.

**Usage:**
```python
from termtint.render import render

styled = StyledString("Hello", style={StyleKey.FOREGROUND: Color.RED})
output = render(styled)
print(output)
```

**Color Control:**
For some usecases it might be desired to be able to ignore all styling. Therefore two functions are provided:
`enable_colors()` enables the rendering of styles while `disable_colors()` disables the rendering of colors. Colors are enabled by default. If deactivated the output of the render function contains no ANSI escape codes.

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

