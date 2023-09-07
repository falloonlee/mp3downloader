# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a falloon`s file.
"""
#导入requests包
import requests

#通过BeautFulSoup获取网页内容
from bs4 import BeautifulSoup

#导入正则
import re

#导入系统
import os



def mp3download(sname,ssrname=''):
     
    #定义搜索链接，通过拼接搜索前导+歌曲名来搜索歌曲
    searchurl="https://zz123.com/search/?key="+longname

    #调用requests.get方法对url进行访问,获取网页以文本的方式存储到searchweb变量中
    searchweb=requests.get(url=searchurl,headers=headers).text
    #编码方式修改为utf-8 支持中文
    #searchweb.encoding='utf-8'
    #利用beautifulsoup解析网页内容
    content=BeautifulSoup(searchweb,"html.parser")

    #判断是否存在itme-info来确认是否搜索到结果,有结果resault不等于None
    resault = content.find_all('div',attrs={'class':'item-info'})
    atag=str(resault)    
    if len(atag) != 2:   # 修改判断格式
        retag = r'<a.*?play/(?P<stag>.*?).htm" title="(?P<sgname>.*?)".*?/singer/.*?title="(?P<srname>.*?)"'
        fresault = re.finditer(retag,atag,re.S)
        for item in fresault:
            songtag=item.group("stag") #歌曲标识
            sgname=item.group("sgname") #歌曲名称
            srname=item.group("srname") #歌手名称
            i = 0
            if ((sgname == sname) | (sgname == sname + srname) | (sgname == srname + sname)| (sgname.startswith(sname))) & (srname.startswith(ssrname)):
                #拼接歌曲下载地址
                songurl="https://zz123.com/xplay/?act=songplay&id="+songtag
                #检差歌曲文件夹是否存在
                fname=srname+'\\'+sname
                folder = os.path.exists(fname)
                if not folder:
                    os.makedirs(fname)
                #读取歌曲
                songres = requests.get(songurl,headers=headers,stream=True)
                #获取文件地址
                singname= sgname+".mp3" #歌曲保持名称.mp3
                file_path = os.path.join(fname,singname) #歌曲保存路径
                print("开始写入文件",file_path)
                #打开本地路径以二进制的方式写入文件，保存到文件夹
                with open(file_path,'wb') as fd:
                    for chunk in songres.iter_content():
                        fd.write(chunk)
                print(sname+"成功下载")
                fd.close()
                
                #获取歌词下载地址        
                lrcurl = "https://zz123.com/geci/" + songtag + ".htm"
                lrcweb = requests.get(lrcurl,headers).text 
                lrccontent = BeautifulSoup(lrcweb,"html.parser")
                lrcres =str(lrccontent.find('div',attrs={'class':'lyric-block'}))
                relrc = r'data-clipboard-text="(?P<lrc>.*?)">'
                lrc = re.finditer(relrc,lrcres,re.S)
                for lr in lrc:
                    lrctxt = lr.group("lrc") 
                    if i==0:
                        lrc_path =os.path.join(fname,sgname+".txt")                
                    else:
                        lrc_path =os.path.join(fname,sgname+".lrc")
                    fb = open(lrc_path,mode='w',encoding='utf-8')
                    fb.write(lrctxt)
                    i = i + 1
                    fb.close()            
                print(sgname,'歌词下载完成')
                break
            else:
                continue
        if i == 0 :
            print("搜到歌曲但无名为",sname,"的歌曲")
    else:        
        print("没有搜到名为",sname,"的歌曲")


#伪装请求头为浏览器标识
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
}

#输入需要搜索的歌曲
longname = input('请输入要搜索的歌曲：\n') 
sname = longname.split(' ')[0]   # 使用空格分割字符串，空格后的字符是歌手名用于确定歌曲
if longname != sname:
    ssrname =longname.split(' ')[1]
    mp3download(sname, ssrname)
else:
    mp3download(sname)





# if len(atag) != 2:
#     retag = r'<a.*?play/(?P<stag>.*?).htm" title="(?P<sgname>.*?)".*?/singer/.*?title="(?P<srname>.*?)"'
#     fresault = re.finditer(retag,atag,re.S)
#     for item in fresault:
#         songtag=item.group("stag") #歌曲标识
#         sgname=item.group("sgname") #歌曲名称
#         srname=item.group("srname") #歌手名称
#         i = 0
#         if (sgname == sname) | (sgname == sname + srname) | (sgname == srname + sname)| (sgname.startswith(sname)):
#             #拼接歌曲下载地址
#             songurl="https://zz123.com/xplay/?act=songplay&id="+songtag
#             #检差歌曲文件夹是否存在
#             fname=srname+'\\'+sname
#             folder = os.path.exists(fname)
#             if not folder:
#                 os.makedirs(fname)
#             #读取歌曲
#             songres = requests.get(songurl,headers=headers,stream=True)
#             #获取文件地址
#             singname= sgname+".mp3" #歌曲保持名称.mp3
#             file_path = os.path.join(fname,singname) #歌曲保存路径
#             print("开始写入文件",file_path)
#             #打开本地路径以二进制的方式写入文件，保存到文件夹
#             with open(file_path,'wb') as fd:
#                 for chunk in songres.iter_content():
#                     fd.write(chunk)
#             print(sname+"成功下载")
#             fd.close()
            
#             #获取歌词下载地址        
#             lrcurl = "https://zz123.com/geci/" + songtag + ".htm"
#             lrcweb = requests.get(lrcurl,headers).text 
#             lrccontent = BeautifulSoup(lrcweb,"html.parser")
#             lrcres =str(lrccontent.find('div',attrs={'class':'lyric-block'}))
#             relrc = r'data-clipboard-text="(?P<lrc>.*?)">'
#             lrc = re.finditer(relrc,lrcres,re.S)
#             for lr in lrc:
#                 lrctxt = lr.group("lrc") 
#                 if i==0:
#                     lrc_path =os.path.join(fname,sgname+".txt")                
#                 else:
#                     lrc_path =os.path.join(fname,sgname+".lrc")
#                 fb = open(lrc_path,mode='w',encoding='utf-8')
#                 fb.write(lrctxt)
#                 i = i + 1
#                 fb.close()            
#             print(sgname,'歌词下载完成')
#             break
#         else:
#             continue
#     if i == 0 :
#         print("搜到歌曲但无名为",sname,"的歌曲")
# else:        
#     print("没有搜到名为",sname,"的歌曲")
