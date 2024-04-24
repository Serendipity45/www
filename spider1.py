import csv
import json

import requests
from bs4 import BeautifulSoup
import datetime
import re

# 定义爬虫函数
def scrape_metrodata1():
    # 定义起始URL
    url = 'https://iwuhan.org/webapps/WuhanMetroFlow/?from=2013-09-04&to=2024-03-24'

    # 发送GET请求获取页面内容
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        # 使用BeautifulSoup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        # 提取script标签中的文本内容
        script_content = soup.findAll('script')
        lenth = len(script_content)
        content = script_content[lenth-1]
        print(type(content))
        content = content.text
        print(content)
        # 去掉 'pipe(' 和 ')'，只保留 JSON 数据部分
        json_data = content.replace('pipe(', '').replace(')', '')

        # 解析 JSON 数据
        data = json.loads(json_data)

        # CSV 文件名
        csv_filename = 'D:\WH_metro\data\data.csv'

        # 写入 CSV 文件
        with open(csv_filename, mode='w', newline='') as csv_file:
            fieldnames = ['date', 'flow']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                writer.writerow({'date': item['date'], 'flow': item['flow']})
        # # 使用正则表达式提取日期和流量数据
        # date1 = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", content)[0]
        # num1 = re.findall(r"\d+\.?\d*", content)[3]
        #
        # # 打印提取的数据
        # print("Date:", date1)
        # print("Flow:", num1)
    else:
        print("Failed to fetch data")

# 执行爬虫函数
scrape_metrodata1()
