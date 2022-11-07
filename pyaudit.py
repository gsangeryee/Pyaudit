import os
from fnmatch import fnmatch
import re


def main():
    # 解析命令行参数

    # 运行分析器，生成分析报告

    # 命令行辅助函数
    
    # FileName + Path
    contests = {}

    root = 'audit'
    file_patterns = "*.sol"
    
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, file_patterns):
                contests[name] = os.path.join(path, name)

    for name, path in contests.items():
        print(name, path)

    code_dict = {}
    # 按行读取 读取行号
    try:
        f = open('audit/2022-05-sturdy/smart-contracts/YieldManager.sol', 'r')
        for i, line in enumerate(f):
            code_dict[line] = i
    finally:
        f.close()
    
    # Read file
    # 该方式读取全部文件到内存中，不适合大文件
    code = ""
    with open('audit/2022-05-sturdy/smart-contracts/YieldManager.sol', 'r') as f:
        code = f.read()
        x = re.findall(r'pragma solidity \^*0\.\d*[1-7].\d*;', code)
        print(x[0])
        for key, value in code_dict.items():
            #print("Key: %s, Value: %d" % (key, value))
            if x[0] in key:
                print("Line Number: %d" % (value))
                break

        

if __name__ == "__main__":
    main()