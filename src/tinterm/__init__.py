import sys

if sys.platform == "win32":
    try:
        import colorama
    except ImportError:
        pass
    else:
        colorama.init()
