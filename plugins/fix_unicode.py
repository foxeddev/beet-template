from beet import Context
import re


def beet_default(ctx: Context):
    """Replace Unicode escape sequences with actual characters in all text files."""

    for function in ctx.data.functions:
        func = ctx.data.functions.get(function)
        if not func:
            continue

        func.text = fix_unicode_escapes(func.text)


def fix_unicode_escapes(text):
    return (
        re.sub(r"\\u([0-9a-fA-F]{5})", lambda m: "\\U" + m.group(1).zfill(8), text)
        .encode("utf-8")
        .decode("unicode_escape")
    )
