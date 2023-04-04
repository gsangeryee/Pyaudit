import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import argparse

def main(url):

    # 将访问令牌存储在环境变量中，或者直接将其替换为字符串
    access_token = os.environ["GITHUB_ACCESS_TOKEN"]
    #print("access_token=",access_token)
    
    # 创建一个字典，用于存放 contest 的路径
    contest_paths = {}
    #如果 url 为空，则从网页获取contest数据：
    if not url:
        # 创建一个 chrome_options 对象
        chrome_options = Options()
        # 添加 "--headless" 选项
        #chrome_options.add_argument("--headless")

        #driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
        # 添加 Chrome 的远程调试地址
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 创建一个 webdriver 对象，传入 chrome_options 参数
        driver = webdriver.Chrome(options=chrome_options)

        driver.get('https://code4rena.com/contests');


        # 定位到包含 "View repo" 内容的 <a> 元素
        elements = driver.find_elements("xpath","//a[contains(text(), 'View repo')]")
        

        print("elements=",elements)
        # 遍历所有元素，打印其 href 属性值
        for element in elements:
            href_value = element.get_attribute("href")
            print("Contest:",href_value)
            # 将 href_value 的结果写入字典中，key 为 href_value 中最后一个 / 之后的内容，value 为 href_value
            contest_paths[href_value.split('/')[-1]] = href_value
        # 关闭浏览器
        driver.quit()
    else:
        # 如果 url 不为空，则从 url 获取 contest 数据
        contest_paths[url.split('/')[-1]] = url

    print("contest_paths=",contest_paths)
    # 下载 contest_paths 中的所有 repo，存放在 audit 文件夹中
    for key in contest_paths:
        # 检查 key 是否在 finished.txt 文件中，如果在，则跳过。否则，下载 repo
        if key in open('finished.txt').read():
            print('finished')
            continue
        else:
            # 从仓库URL中提取用户名和仓库名
            repo_url = contest_paths[key]
            username, repo_name = repo_url.split('/')[-2:]
            # 使用访问令牌克隆仓库
            os.system(f'git clone https://{access_token}@github.com/{username}/{repo_name}.git audit{os.sep}{key}')
            # 下载 repo
            #os.system('git clone ' + contest_paths[key] + ' audit' + os.sep + key)
            
            # 将 key 写入 finished.txt 文件中，用逗号分隔。如果文件不存在，则创建文件
            with open('finished.txt', 'a') as f:
                f.write(key + ',')
                f.close()
            #开始自动Audit 
            # 解析 README.md 文件，获取所有范围内合约的路径
            pattern1 = r"\|\s(\S+\.sol)\s\|"
            pattern2 = r"\|\s+\[(\S+\.sol)\]\((\S+.sol)\)"
            #读取目录key下的README.md文件
            with open('audit' + os.sep + key + os.sep + 'README.md',"r") as f:
            #按行读取文件内容
                #print('audit' + os.sep + key + os.sep + 'README.md')
                result = []
                for line in f:
                    #使用正则表达式匹配
                    match1 = re.match(pattern1,line)
                    if match1:
                        # 将匹配结果存入list中
                        result.append(match1.group(1))
                    match2 = re.match(pattern2,line)
                    if match2:
                        # 因为group(1)的路径有时不完整，需要使用group(2)的完整路径
                        # 取得文件链接
                        sol_href = match2.group(2)
                        # 截取连接中 main/ 之后的内容，即为合约路径
                        sol_path = sol_href.split('main/')[1]
                        # 将匹配结果存入list中
                        result.append(sol_path)
                # 将list中的内容按行写入scope.txt文件中，写入前先清空文件内容，如果文件不存在，则创建文件。
                with open('scope.txt', 'w') as f:
                    f.write('\n'.join(result))
                    f.close()
                # 运行 pyaudit.py
                # 设置 url 参数
                url = contest_paths[key] + '/tree/main/'
                # 设置 contest 参数
                contest = key
                # 运行 pyaudit.py
                os.system('python pyaudit.py -c ' + contest + ' -u ' + url)

if __name__ == '__main__':
    # add parser arguments for url, it is optional
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url of the contest', default='')
    args = parser.parse_args()
    contest_url = args.url
    main(contest_url)
