import re

term_colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    "reset": "\033[0m",
}


def printc(text, color="white", **kwargs):
    text = f"{term_colors[color]}{text}{term_colors['reset']}"
    print(text, **kwargs)


def make_filename(raw_name: str, raw_ext: str) -> str:
    """
    Sanitize a file name
    """
    invalid_chars = r'[\s.<>:"/\\|?*\x00-\x1f]'
    replacement_char = "_"
    name = re.sub(invalid_chars, replacement_char, raw_name).strip(replacement_char)
    ext = re.sub(invalid_chars, replacement_char, raw_ext).strip(replacement_char)
    if (not name) or (not ext):
        raise ValueError(
            f'Could not turn the string "{raw_name}" and the extension "{raw_ext}" into a valid filename'
        )
    filename = (name + "." + ext).lower()
    return filename
