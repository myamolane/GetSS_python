import simplejson as json
import requests
from bs4 import BeautifulSoup
import re
from sys import path

def request(url):
    headers={'User-Agent':
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    content=requests.get(url,headers=headers)
    return content


def get_soup(url):
    html=request(url)   
    soup=BeautifulSoup(html.text,'lxml')
    
    return soup

def read_json(path):
    with open(path,'r') as json_file:
        content=json.load(json_file)
        json_file.close()
        return content
def write_json(path,content):
    with open(path,'w') as json_file:
        json.dump(content,json_file,indent=4)
        json_file.close()
def get_json_value(path,key):
    content=read_json(path)
    return content[key]
def set_json_value(path,key,value):
    content=read_json(path)
    content[key]=value
    write_json(path,content)
    return content
def fix_path(file_name):
    return path[0]+"\\"+file_name
def request_baidu(key):
    soup=get_soup('http://www.baidu.com/s?wd='+key)
    rec=soup.find('div',id="1").find('a')['href']
    response=request(rec)
    return response

def get_ss(key):
    print(path[0])
    search_key='iss'
    url=get_json_value(fix_path('config.json'),'url')
    try:
        soup=get_soup(url)
    except:
        response=request_baidu(search_key)
        soup=BeautifulSoup(response.text,'lxml')
        set_json_value(fix_path('config.json'),'url',response.url)
    # div=soup.find_all('div',class_="col-sm-4 text-center")
    div=soup.find_all('div',class_="portfolio-item")
    
    ss_list=[]
    for each_div in div:
        h4=each_div.find_all('h4')
        dic={}
        n=0
        for each_h4 in h4:
            value=re.search(r'([-\.\w ]+)$',each_h4.text)
            if (value!=None):
                if (n==4):
                    ss_list.append(dic)
                    n=0
                else:
                    
                    dic[key[n]]=value.group(1).strip()
                    print(dic[key[n]]+":"+str(n))
                    n=n+1
    
    return ss_list   
def save_config(ss_list,key,file_name):
    index=[]
    content=read_json(file_name)
    
    for j in range(len(ss_list)):
        flag=False
        for i in range(len(content["configs"])):
            if (content["configs"][i]["server"]==ss_list[j]["server"]):
                flag=True
                for k in range(1,len(key)):
                    if (content["configs"][i][key[k]]!=ss_list[j][key[k]]):
                        content["configs"][i][key[k]]=ss_list[j][key[k]]
                break
        if flag==False:
            index.append(j)
    for _index in index:
        content["configs"].append(ss_list[_index])
    write_json(file_name,content)


def make_config():

    key=["server","server_port","password","method"]
    file_name=get_json_value(fix_path('config.json'),'filename')
    save_config( get_ss(key) ,key,fix_path(file_name))  
make_config()

