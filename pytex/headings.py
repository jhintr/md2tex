import re


def find_toml(frontmatter, kw):
    """
    kw: keyword in frontmatter, like `title`, `section` etc
    """

    _re = r"^%s: (.*)$" % kw
    _ma = re.search(_re, frontmatter, re.MULTILINE)
    if _ma:
        result = _ma.group(1)
        result = result.strip('"').strip("'")
        return result
    return ""


def frontmatter(contents: str, title_is_chapter: bool = True):
    """
    if `title_is_chapter` then
        `title` to `\chapter{}` & ignore `section`,
    else
        `title` to `\section{}` & `section` to `\chapter{}`
    """

    fm_re = r"^---\n(.*?)\n---\n"
    match = re.search(fm_re, contents, re.DOTALL)
    if match:
        frontmatter = match.group(0)

        text = find_toml(frontmatter, "title")

        if title_is_chapter:
            text = r"\\chapter{%s}\n" % text
        else:
            text = r"\\section{%s}\n" % text

            section = find_toml(frontmatter, "section")
            if section:
                text = r"\\chapter{%s}\n\n" % section + text

        contents = re.sub(fm_re, text, contents, flags=re.DOTALL)
    return contents


def heading(contents: str, h4h5: str):
    """
    change `### ` or `#### ` to `section` or `subsection`
    """

    def _proc(heading: str, dest: str):
        # remove anything after {}, which is heading's id in html
        text = heading.split("{")[0].strip()
        text = "\%s{%s}" % (dest, text)
        return text

    _re = r"%s (.*)" % h4h5
    _dest = "section" if h4h5 == "###" else "subsection*"
    contents = re.sub(_re, lambda match: _proc(match.group(1), _dest), contents)
    return contents
