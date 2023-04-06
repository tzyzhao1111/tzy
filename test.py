# -*- coding: utf-8 -*-
import requests
import re
import json
import time

# 请在这里填入你的cookie、user-agent和appmsg_token
cookie = ""
user_agent = ""
appmsg_token = ""

# 请在这里填入你想爬取的公众号名称
gzh_name = "阅读者陈安培"

# 请在这里填入你想爬取的公众号文章数量
num = 10

# 获取公众号的url和fakeid
def get_url_fakeid(gzh_name):
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz?"
    params = {
        "action": "search_biz",
        "token": "",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "query": gzh_name,
        "begin": "0",
        "count": "5"
    }
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
        "Referer": "https://mp.weixin.qq.com/"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data["base_resp"]["ret"] == 0:
        for item in data["list"]:
            if item["nickname"] == gzh_name:
                return item["url"], item["fakeid"]
    else:
        print("获取公众号信息失败，请检查cookie是否有效")

# 获取文章列表
def get_article_list(url, fakeid):
    article_list = []
    begin = 0
    while True:
        url = url + "&begin=" + str(begin) + "&count=5"
        headers = {
            "Cookie": cookie,
            "User-Agent": user_agent,
            "Referer": url
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if data["base_resp"]["ret"] == 0:
            for item in data["app_msg_list"]:
                article_list.append(item)
            if len(article_list) >= num or data["app_msg_cnt"] == len(article_list):
                break
            else:
                begin += 5
                time.sleep(1)
        else:
            print("获取文章列表失败，请检查cookie是否有效")
            break
    return article_list

# 获取文章阅读数和点赞数
def get_read_like(appmsgid, itemidx):
    url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    params = {
        "__biz": fakeid,
        "appmsgid": appmsgid,
        "itemidx": itemidx,
        "scene": 27,
        "is_only_read": 1,
        "is_temp_url": 0,
        "reward_uin_count": 0,
        "__biz": fakeid,
        "__key__":"",
        "__pass_ticket__":"",
        "__appmsg_token__":"",
    }
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
        "Referer":"https://mp.weixin.qq.com/s?__biz="+fakeid+"&mid="+appmsgid+"&idx="+itemidx+"&sn=",
    }
    response = requests.post(url, params=params, headers=headers)
    data = response.json()
    if data["base_resp"]["ret"] == 0:
        return data["appmsgstat"]["read_num"], data["appmsgstat"]["like_num"]
    else:
        print("获取阅读数和点赞数失败，请检查cookie、user-agent和appmsg_token是否有效")

# 主函数
if __name__ == "__main__":
    # 获取公众号的url和fakeid
    url, fakeid = get_url_fakeid(gzh_name)
    
    # 获取文章列表
    article_list = get_article_list(url, fakeid)
    
    # 打印文章标题、链接、阅读数和点赞数
    for article in article_list:
        appmsgid = article["aid"]
        itemidx = article["itemidx"]
        title = article["title"]
        link = article["link"]
        
        read_num, like_num = get_read_like(appmsgid, itemidx)
        
        print(title)
        print(link)
        print("阅读数：", read_num)
        print("点赞数：", like_num)
        print("-"*50)