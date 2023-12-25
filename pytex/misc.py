import re


def remove_link(contents):
    """
    remove `<a>` and `{{<suttalink>}}`
    """
    contents = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", contents)

    # remove suttalink
    sutta_re = r"\{\{<suttalink src=\"(.*?)\">\}\}(.*)\{\{</suttalink>\}\}"
    contents = re.sub(sutta_re, r"\2", contents)

    return contents


def make_footnote(contents):
    """
    NOTICE: fn markers in `.md` shouldn't be duplicated
    """

    fn_list = re.findall(
        r"^(\[\^\d+\]): (.*?)$",
        contents,
        flags=re.MULTILINE,
    )
    for fn in fn_list:
        _marker, _note = fn
        full_fn = ": ".join(fn)
        contents = contents.replace(full_fn, "")
        contents = contents.replace(_marker, r"\footnote{%s}" % _note)
    return contents


def bolded_normal_para(match):
    """
    bolden text not surrounded by `<small>`
    """
    text = match.group(0)
    text = re.split(r"(<small>.*?</small>)", text)
    text = [t if t.startswith("<small>") else r"\textbf{%s}" % t for t in text]
    text = "".join(text).replace(r"\textbf{}", "")
    return text


def remove_n_blank(contents):
    """
    remove \n\n\n
    """

    _re = r"\n\n\n"
    contents = re.sub(_re, r"\n\n", contents)
    if re.search(_re, contents, flags=re.MULTILINE):
        contents = remove_n_blank(contents)
    return contents


def multilines(contents):
    """
    replace multilines
    """

    sign_re = r"^\{\{<sign>\}\}(.*)\{\{</sign>\}\}$"
    sign_pa = r"%%\begin{flushright}%s\end{flushright}"

    quot_re_ = r"^> - (.*)$"
    quot_re = r"^> (.*)$"
    quot_pa = r"\begin{quoting}%s\end{quoting}"

    subtitle_re = r"^\{\{<subtitle>\}\}(.*)\{\{</subtitle>\}\}$"
    subtitle_pa = r"\begin{center}%s\end{center}\vspace{1em}"

    q_re = r"<q>(.*?)</q>$"
    q_pa = r"\hfill\textcolor{gray}{\footnotesize %s}"

    multilines = {
        sign_re: sign_pa,
        quot_re_: quot_pa,
        quot_re: quot_pa,
        subtitle_re: subtitle_pa,
        q_re: q_pa,
    }
    for regex, patt in multilines.items():
        contents = re.sub(
            regex,
            lambda match: patt % match.group(1),
            contents,
            flags=re.MULTILINE,
        )
    return contents


def inlines(contents):
    inlines = {
        r"`(.*?)`": r"\texttt{%s}",
        r"\*\*(.*?)\*\*": r"\textbf{%s}",
        r"\*(.*?)\*": r"\textit{%s}",
        r"<em>(.*?)</em>": r"\textit{%s}",
        r"<small>(.*?)</small>": r"{\footnotesize %s}",
        r"<sup>(.*?)</sup>": r"\textsuperscript{%s}",
        r"<a href=\".*?\">(.*?)</a>": r"%s",
    }
    for regex, patt in inlines.items():
        contents = re.sub(regex, lambda match: patt % match.group(1), contents)
    return contents


def replace_shortcode(contents: str, tag: str, dest: str, ex: str):
    """
    replace hugo shortcode
    """

    contents = re.sub(
        r"\{\{<%s>\}\}" % tag,
        r"\\begin{%s}%s" % (dest, ex),
        contents,
        flags=re.MULTILINE,
    )
    contents = re.sub(
        r"\{\{</%s>\}\}" % tag,
        r"\\end{%s}" % dest,
        contents,
        flags=re.MULTILINE,
    )

    return contents
