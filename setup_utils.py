import os
import re
from io import open

ROOT = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_NAME = os.path.basename(ROOT)
PACKAGE_NAME = DIRECTORY_NAME.replace("-", "_")
RE_VARIABLE = r"{} = ['\"]([^'\"]*)['\"]"
RE_README_SECTION_HEADING = r"#+ {}"
RE_README_SECTION = r"{}[^#]*"
RE_NEWLINES = r"{}\n+"


def read_section(path, title, sentences=(0,)):
    content = read(path)
    heading_regex = RE_README_SECTION_HEADING.format(title)
    section_regex = RE_README_SECTION.format(heading_regex)
    newline_regex = RE_NEWLINES.format(heading_regex)
    match = re.search(section_regex, content)
    try:
        desc = match.group(0)
        desc = desc.strip()
        desc = re.sub(newline_regex, "", desc)
        parts = desc.split(".")
        desc = ". ".join([x for x in parts if parts.index(x) in sentences])
        desc = desc.strip()
    except AttributeError:
        desc = ""
    return desc


def read(parts, variable=None):
    path = os.path.join(ROOT, *parts)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if variable is None:
        return content
    regex = RE_VARIABLE.format(variable)
    match = re.search(regex, content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Failed to read {} in {}".format(variable, path))

