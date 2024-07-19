import os
import re


def count():
    """
    计算义注对三藏的引用
    输出：引用名及其次数
    """

    input_dir = r"../ehipassa/content/atthakatha/"
    dirs = [
        "dhammapadatthakatha/",
        "kankhavitarani/",
        "manorathapurani/",
        "papancasudani",
        "paramatthajotika/",
        "samantapasadika/",
        "saratthappakasini/",
        "sumangalavilasini/",
        "visuddhimagga/",
    ]
    out_file = "akrefs.csv"
    out_dict = {}

    ignores = [
        ".DS_Store",
        "_index.md",
    ]

    for dir in dirs:
        source = input_dir + dir
        for filename in os.listdir(source):
            if filename in ignores:
                continue
            with open(os.path.join(source, filename), "r") as f:
                try:
                    contents = f.read()
                except:
                    print(source, filename)
                    continue

            out_dict = entry(contents, out_dict)

    with open(out_file, "w") as out:
        out.write("Ref,Count")
        # sort
        out_dict = dict(sorted(out_dict.items(), key=lambda x: x[1], reverse=True))
        for k, v in out_dict.items():
            out.write("\n" + k + "," + str(v))


def entry(contents, out_dict):
    """
    处理条目
    """

    refs = re.findall(r"<small>\((.*?)\)</small>", contents)
    for entry in refs:
        entry = re.split(";", entry)  # 每条引用也许包含多个来源
        for e in entry:
            e = e.strip().lower()
            e = re.split(r" \d", e)[0]  # 去除数字部分
            if e[0].isdigit():
                continue  # 若以数字开头，略过
            if e.startswith("cūḷani."):
                e = "cūḷani."  # 小义释需要省略后面的章节

            # todo 还有很多需要处理

            if e not in out_dict:
                out_dict[e] = 1
            else:
                out_dict[e] += 1
    return out_dict


if __name__ == "__main__":
    count()
