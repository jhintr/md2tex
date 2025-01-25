import re


def gatha_number(contents):
    """
    add PTS number to subsection
    """

    def _proc(_num: str):
        num = int(_num)
        if num < 164:
            return r"\subsection\*{\textbf{%s}}" % (_num)
        if num == 164:
            num = "163A"
        elif num == 165:
            num = "163B"
        elif num <= 232:
            num -= 2
        elif num == 233:
            num = r"231\textit{a-d}"
        elif num == 234:
            num = r"231\textit{e-h}"
        elif num <= 459:
            num -= 3
        elif num == 460:
            num = r"457\textit{a-b}"
        elif num == 461:
            num = r"457\textit{c-f}"
        elif num == 462:
            num = r"458\textit{a-c}"
        elif num == 463:
            num = r"458\textit{d-e}"
        elif num <= 498:
            num -= 5
        elif num == 499:
            num = r"494\textit{a-d}"
        elif num == 500:
            num = r"494\textit{e-h}"
        elif num <= 767:
            num -= 6
        elif num == 768:
            num = r"762\textit{a-d}"
        elif num == 769:
            num = r"762\textit{ef}-763\textit{ab}"
        elif num == 770:
            num = r"763\textit{c-f}"
        else:
            num -= 7
        return r"\subsection\*{\textbf{%s} \textcolor{gray}{\footnotesize 〔PTS %s〕}}" % (
            _num,
            num,
        )

    _re = r"\\subsection\*{(\d+)}"
    contents = re.sub(_re, lambda match: _proc(match.group(1)), contents)
    return contents
