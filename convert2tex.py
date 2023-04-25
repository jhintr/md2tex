import os
import re


def make_chapter(contents):
    """
    find the frontmatter and replace `title: ""` to `\chapter{}`
    """
    fm_re = r"^---\n(.*?)\n---\n"
    match = re.search(fm_re, contents, re.DOTALL)
    if match:
        frontmatter = match.group(0)
        title_re = r"^title: (.*)$"
        title_match = re.search(title_re, frontmatter, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            title = r"\\chapter{%s}\n" % title.strip('"').strip("'")
            contents = re.sub(fm_re, title, contents, flags=re.DOTALL)
    return contents


def make_section(contents):
    """
    replace `#### ` to `\section{}`
    """

    def proc_sect(sect):
        # remove anything after {}
        text = sect.split("{")[0].strip()
        # if has <small> tag, change to \section
        if "<small>" in sect:
            text = text.split(" ")
            text0 = "\section{%s}" % text[0]
            text1 = (
                text[1].replace("<small>", "%{\\footnotesize ").replace("</small>", "}")
            )
            text = text0 + "\n\n" + text1
        # otherwise, to \section*
        else:
            text = "\section*{%s}" % text
        return text

    sect_re = r"#### (.*)"
    contents = re.sub(sect_re, lambda match: proc_sect(match.group(1)), contents)
    return contents


def make_subsection(contents):
    """
    replace `##### ` to `\subsection{}`
    """

    def proc_sub(sect):
        text = sect.split("{")[0].strip()
        text = "\subsection*{%s}" % text
        return text

    sub_re = r"##### (.*)"
    contents = re.sub(sub_re, lambda match: proc_sub(match.group(1)), contents)
    return contents


def convert2tex(source: str, bold: bool = False):
    """Convert `.md` files to `.tex`.

    Parameters:
        source: source dir in ehipassa/content/, e.g. "classic/shi"
        bold: if set normal para text to boldface
    """
    _source = source.strip("/")
    _source_last = _source.split("/")[-1]
    input_dir = r"../ehipassa/content/" + _source
    output_dir = "content/" + _source_last

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".md") and not filename.startswith("_"):
            with open(os.path.join(input_dir, filename), "r") as f:
                contents = f.read()

            contents = make_chapter(contents)
            contents = make_subsection(contents)
            contents = make_section(contents)

            # remove 詩譜
            contents = re.sub(r"^> \[\*\*詩譜.*$", "", contents, flags=re.MULTILINE)

            # deal with footnote
            # on one condition: fn markers in .md shouldn't duplicate
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

            # remove hyperlinks
            contents = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", contents)

            # deal with multilines
            sign_re = r"^\{\{<sign>\}\}(.*)\{\{</sign>\}\}$"
            sign_pa = r"%%\begin{flushright}%s\end{flushright}"

            quot_re = r"^> (.*)$"
            quot_pa = r"\begin{quoting}%s\end{quoting}"

            multilines = {
                sign_re: sign_pa,
                quot_re: quot_pa,
            }
            for regex, patt in multilines.items():
                contents = re.sub(
                    regex,
                    lambda match: patt % match.group(1),
                    contents,
                    flags=re.MULTILINE,
                )

            # deal with normal para: after multilines, so not starts with `\`
            def proc_para(match):
                """if text not in the `<small>`, bold it"""
                text = match.group(0)
                text = re.split(r"(<small>.*?</small>)", text)
                text = [
                    t if t.startswith("<small>") else r"\textbf{%s}" % t for t in text
                ]
                text = "".join(text).replace(r"\textbf{}", "")
                return text

            if bold and filename != "shi-pu.md":
                contents = re.sub(
                    r"^([^\\\n\%])(.*)$",  # not starts with `\` or `\n` or `%`
                    lambda match: proc_para(match),
                    contents,
                    flags=re.MULTILINE,
                )

            # deal with inline stuff
            inlines = {
                r"`(.*?)`": r"\texttt{%s}",
                r"\*\*(.*?)\*\*": r"\textbf{%s}",
                r"<small>(.*?)</small>": r"{\footnotesize %s}",
            }
            for regex, patt in inlines.items():
                contents = re.sub(regex, lambda match: patt % match.group(1), contents)

            # deal with multiple blank lines
            def remove_n_blank(contents):
                """remove \n\n\n"""
                regex = r"\n\n\n"
                contents = re.sub(regex, r"\n\n", contents)
                if re.search(regex, contents, flags=re.MULTILINE):
                    contents = remove_n_blank(contents)
                return contents

            contents = remove_n_blank(contents)

            out_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".tex")
            with open(out_file, "w") as f:
                f.write(contents)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Convert `.md` files to `.tex`.")
    parser.add_argument(
        "source",
        type=str,
        help="specify source dir in ehipassa/content/, e.g. `classic/shi`",
    )
    parser.add_argument(
        "-b",
        "--bold",
        action="store_true",
        help="set normal para text to boldface",
    )
    args = parser.parse_args()

    convert2tex(args.source, args.bold)
