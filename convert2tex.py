import os
import re
from pytex.headings import frontmatter, heading
from pytex.misc import (
    bolded_normal_para,
    inlines,
    make_footnote,
    multilines,
    remove_link,
    remove_n_blank,
    replace_shortcode,
)
from pytex.snp import gatha_number


def convert2tex(source: str, bold: bool = False, is_section: bool = False):
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

            contents = frontmatter(contents, not is_section)
            contents = heading(contents, "#####")
            contents = heading(contents, "####")

            # 例外：删除 /shi 中「詩譜」的链接
            contents = re.sub(r"^> \[\*\*詩譜.*$", "", contents, flags=re.MULTILINE)

            # 删除 namo
            contents = re.sub(r"^\{\{<namo>\}\}$", "", contents, flags=re.MULTILINE)

            contents = make_footnote(contents)
            contents = remove_link(contents)

            # replace eof with center
            contents = replace_shortcode(contents, "eof", "center", r"\\vspace{1em}")
            contents = replace_shortcode(contents, "bqgatha", "quoting", "")

            # replace <br> with \\
            contents = re.sub(r"  $", r"\\\\", contents, flags=re.MULTILINE)
            contents = re.sub(r"<br>", r"\\\\", contents)

            contents = multilines(contents)

            # 加粗正文段落：即不以 `\`,`\n`,`%` 开头的段落
            except_md = ["shi-pu.md"]
            if bold and filename not in except_md:
                contents = re.sub(
                    r"^([^\\\n\%])(.*)$",
                    lambda match: bolded_normal_para(match),
                    contents,
                    flags=re.MULTILINE,
                )

            contents = inlines(contents)
            contents = remove_n_blank(contents)
            contents = gatha_number(contents)

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
    parser.add_argument(
        "-s",
        "--section",
        action="store_true",
        help="set title to section",
    )
    args = parser.parse_args()

    convert2tex(args.source, args.bold, args.section)
