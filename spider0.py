'''
抓取并保存 正文、图片、发布时间、点赞数、评论数、转发数
抓取的微博id：
洋葱故事会   https://m.weibo.cn/u/1806732505
'''


# -*-coding:utf8-*-
# 需要的模块
import datetime
import os
import urllib
import urllib.request
import time
import json

import pymysql
import xlwt

# 定义要爬取的微博大V的微博ID
id='3186945861'

# 设置代理IP
proxy_addr="165.225.76.79"



# 定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    print(data)
    return data

# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid

# 获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')
    urank=content.get('userInfo').get('urank')
    print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" +  "粉丝数：" + str(fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")
    return name
from dateutil import parser
# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file):
    i=1
    m=534
    flag=0
    # 使用 connect 方法，传入数据库地址，账号密码，数据库名就可以得到你的数据库对象
    # now_time = datetime.datetime.now()
    # time1 = (now_time+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

    # 插入一条记录

    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        print(weibo_url)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            print(content)
            cards=content.get('cards')
            print(len(cards))
            if(len(cards)>0):
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')

                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        time_id = mblog.get('created_at')
                        print(type(time_id))
                        parsed_time = parser.parse(time_id)

                        # 将解析后的时间对象转换为斜杠形式的日期字符串
                        date_str_slash_format = parsed_time.strftime("%Y/%m/%d")

                        print(date_str_slash_format)
                        text=mblog.get('text')						  # 微博内容
                        result=text.find('昨日客流')
                        if result>0:
                            state_data1=[]
                            content1=text.replace("：",";")
                            content1=content1.replace("、",";")
                            content1=content1.replace("。",";")
                            state=content1.split(";")
                            state_data1.append(state[1])
                            state_data1.append(state[2])
                            state_data1.append(state[3])
                            state_data1.append(state[4])
                            state_data1.append(state[5])

                            content2=text.replace("【昨日客流】","")
                            print(content2)
                            content2 = content2.replace("月",";")
                            print(content2)
                            content2 = content2.replace("日",";")
                            date1 = content2.split(";")
                            time1=date1[0]+date1[1]
                            content3 = text.replace("【昨日客流】","")
                            content3 = content3.replace("为",";")
                            content3 = content3.replace("万乘次",";")
                            data2 = content3.split(";")
                            flow = data2[1]
                            print(flow)
                            print(time1)
                            print(state_data1)
                            with open(file,'a',encoding='utf-8') as fh:
                                fh.write(date_str_slash_format+'\t'+state_data1[0]+'\t'+state_data1[1]+'\t'+state_data1[2]+'\t'+state_data1[3]+'\t'+state_data1[4]+'\t'+flow+'\t'+'\n')
                            #     fh.write(text+'\n')
                            db = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="metro_new",charset='utf8')
                            # 接着我们获取 cursor 来操作我们的 avIdol 这个数据库
                            cursor = db.cursor()
                            # time1 = (now_time+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

                            sql = "insert into Daysort(date,one, two,three,four,five) values ('%s','%s','%s','%s','%s','%s')" %(time1,state_data1[0],state_data1[1],state_data1[2],state_data1[3],state_data1[4])

                            flag=flag+1
                            try:
                                cursor.execute(sql)
                                db.commit()
                            except:
                                # 回滚
                                db.rollback()
                    # if flag==1:
                    #     break

                i+=1
                '''休眠1s以免给服务器造成严重负担'''
                time.sleep(1)
            else:
                break
        except Exception as e:
            print(e)
            pass
        if flag==1:
            break



def txt_xls(filename,xlsname):
    """
    :文本转换成xls的函数
    :param filename txt文本文件名称、
    :param xlsname 表示转换后的excel文件名
    """
    try:
        with open(filename,'r',encoding='utf-8') as f:
            xls=xlwt.Workbook()
            #生成excel的方法，声明excel
            sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True)
            # 页数、条数、微博地址、发布时间、微博内容、点赞数、评论数、转发数
            sheet.write(0, 0, '时间')
            sheet.write(0, 1, 'one')
            sheet.write(0, 2, 'two')
            sheet.write(0, 3, 'three')
            sheet.write(0, 4, 'four')
            sheet.write(0, 5, 'five')
            sheet.write(0, 6, 'flow')
            # sheet.write(0, 6, '评论数')
            # sheet.write(0, 7, '转发数')
            # sheet.write(0, 8, '图片链接')
            x = 1
            while True:
                #按行循环，读取文本文件
                line = f.readline()
                if not line:
                    break  #如果没有内容，则退出循环
                for i in range(0, len(line.split('\t'))):
                    item=line.split('\t')[i]
                    sheet.write(x,i,item) # x单元格行，i 单元格列
                x += 1 #excel另起一行
        xls.save(xlsname) #保存xls文件
    except:
        raise



if __name__=="__main__":
    name = get_userInfo(id)
    file = str(name) + id+"_new1.txt"
    get_weibo(id,file)

    txtname = file
    xlsname = str(name) + id + "_new1.xls"
    txt_xls(txtname, xlsname)

print('finish')


 