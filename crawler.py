import requests
import json
import csv
from fake_useragent import UserAgent
import time
# import random

def main():
    headers= {'User-Agent': str(UserAgent(use_cache_server=False).random)}
    # 定义URL
    url = "http://12345.sanya.gov.cn/u/sy1/newConsult/viewOrdersInfo?keyword=&no=&deptId=12345&page=%d&pageSize=10&wpType="
    urlToInfo = "http://12345.sanya.gov.cn/u/sy1/newConsult/viewOrderNoOpenDetail?no="

    # 请求第一页读取总页数
    response = requests.get(url=format(url % 1), headers=headers).json()
    # print(response)
    totalPage = response['totalPage']
    # print(totalPage)

    # 创建输出文件并写入表头
    fp = 'E:\\12345_Data.csv'
    with open(fp, 'a+', encoding='utf-8', newline='') as f:
        csv_write = csv.writer(f)
        data_row = ["id", "所属类别", "来源", "开始时间", "所属类型", "备注", "详细信息", "下一站", "是否推迟", "延迟数", "延迟原因", "满意度"]
        csv_write.writerow(data_row)

        # 取每一页的wpid并跳转到相应的detailInfo页面，获得json数据，提取需要的信息调整格式进行输出
        for page in range(1, totalPage+1):
            response = requests.get(url=format(url % page), headers=headers).json()
            pageSize = response['pageSize']
            for item in range(pageSize):

                no = response['data']['wpInfos'][item]['wpid']
                print("正在写入单号为"+no+"的数据")
                responseToInfo = requests.get(url=urlToInfo+no, headers=headers).json()
                # print(responseToInfo)
                # exit(0)
                try:
                    data_row = [responseToInfo['data']['wpInfo']['wpid'], responseToInfo['data']['wpInfo']['class1'],
                                responseToInfo['data']['wpInfo']['wpSource'], responseToInfo['data']['wpInfo']['starttime'],
                                responseToInfo['data']['wpInfo']['wpType'], responseToInfo['data']['wpInfo']['note'],
                                responseToInfo['data']['wpInfo']['summary'], responseToInfo['data']['wpInfo']['nextState'],
                                responseToInfo['data']['wpInfo']['isDelay'], responseToInfo['data']['wpInfo']['delayNum'],
                                responseToInfo['data']['wpInfo']['delayReason'],
                                responseToInfo['data']['wpInfo']['satisfaction']]
                    csv_write.writerow(data_row)
                    time.sleep(1)
                except :
                    continue

        f.close()
        print("--------------------------数据爬取完成---------------------------------")

if __name__ == '__main__':
    main()
