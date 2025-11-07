import glob
import re

# 获取当前路径下所有匹配 1**.tex 的文件
files = glob.glob("5**.tex")

# 提取文件名中的数字部分并排序
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

files.sort(key=extract_number)

# 合并写入 v5.tex
with open("v5.tex", "w", encoding="utf-8") as outfile:
    for fname in files:
        with open(fname, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())

print(f"✅ 合并完成，共 {len(files)} 个文件，输出为 v5.tex")
