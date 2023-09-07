# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 21:04:10 2023
UI mp3downloader from file
This is a falloon`s file.
@author: yufen
"""


import tkinter as tk # tkinter库 可以显示界面
from tkinter import filedialog # 从tk中引入 filedialog 用以浏览文件夹
#导入requests包
import requests

#通过BeautFulSoup获取网页内容
from bs4 import BeautifulSoup

#导入正则
import re

#导入系统
import os,time
    

####################################浏览文件子函数##############################    
def scan():
    filetypes = [("txt文本文件", "*.txt")]
    file_name= filedialog.askopenfile(title='选择单个文件',filetypes=filetypes,initialdir='./')
    path_avr.set(file_name.name) # .name 仅仅显示文件路径，不显示＜_io.TextIOWrapper name=‘*‘ mode=‘r‘ encoding=‘utf-8‘＞

###############################################################################

####################################清除文件子函数##############################    
def d_scan():
    path_avr.set("") # 把文件路径文本框内容设置为空
###############################################################################

####################################浏览文件夹子函数##############################    
def oscan():
    
    file_op= filedialog.askdirectory() #打开文件夹
    op_avr.set(file_op)
###############################################################################

####################################清除文件子函数##############################    
def do_scan():
    op_avr.set("") # 把文件路径文本框内容设置为空
###############################################################################

####################################歌名获取子函数##############################
def mp3_dl():
    
    ############################单个歌曲下载子函数######################################
    def mp3download(op_avr,sname,ssrname=''):
        #定义搜索链接，通过拼接搜索前导+歌曲名来搜索歌曲
        searchurl="https://zz123.com/search/?key="+longname
        headers={
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Authority':'zz123.com',

            'Upgrade-Insecure-Requests':'1',
            'Referer':'https://zz123.com/search/?key='+sname.encode("utf-8").decode("latin1"),
        	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
        }
        
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
                    fname=op_avr.get().replace('/','\\')+'\\'+srname+'\\'+sname
                    print(fname)
                    folder = os.path.exists(fname)
                    if not folder:
                        os.makedirs(fname)
                    #读取歌曲
                    songres = requests.get(songurl,headers=headers,stream=True)
                    #获取文件地址
                    singname= sgname+".mp3" #歌曲保持名称.mp3

                    file_path = os.path.join(fname,singname) #歌曲保存路径
                    dl_res.insert('end',"开始写入文件"+file_path)
                    dl_res.update()#刷新文本框显示
                    #打开本地路径以二进制的方式写入文件，保存到文件夹
                    with open(file_path,'wb') as fd:
                        for chunk in songres.iter_content():
                            fd.write(chunk)
                    dl_res.insert('end',"\n"+sname+"成功下载,文件存储在"+file_path)
                    dl_res.update()#刷新文本框显示
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
                    dl_res.insert('end',"\n"+sgname+'歌词下载完成'+"\n"+"下载完成！！！\n")
                    dl_res.update()#刷新文本框显示
                    break
                else:
                    continue
            if i == 0 :
                dl_res.insert('end',"\n搜到歌曲但无名为《"+sname+"》的歌曲\n")
                dl_res.update()#刷新文本框显示
        else:        
            dl_res.insert('end',"\n没有搜到名为《"+sname+"》的歌曲\n")
            dl_res.update()#刷新文本框显示


    ##################################################################################
    
    #############################歌曲单下载子函数######################################
    def mp3listdownload(op_avr,sname,cc,ssrname=''):
        
        dl_res.insert('end',"第"+str(cc)+"首歌："+sname+"\n")
        dl_res.update()#刷新文本框显示
        if cc != 1:    
            time.sleep(15)
        #定义搜索链接，通过拼接搜索前导+歌曲名来搜索歌曲
        searchurl="https://zz123.com/search/?key="+sname
        #伪装请求头为浏览器标识
        headers={
         	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
        }
        #调用requests.get方法对url进行访问,获取网页以文本的方式存储到searchweb变量中
        
        searchweb=requests.get(url=searchurl,headers=headers).text
        #编码方式修改为utf-8 支持中文
        #searchweb.encoding='utf-8'
        #利用beautifulsoup解析网页内容
        content=BeautifulSoup(searchweb,"html.parser")
        
        #判断是否存在itme-info来确认是否搜索到结果,有结果resault不等于None
        resault = content.find_all('div',attrs={'class':'item-info'})
        atag=str(resault)
        if len(atag) != 2:
            retag = r'<a.*?play/(?P<stag>.*?).htm" title="(?P<sgname>.*?)".*?/singer/.*?title="(?P<srname>.*?)"'
            fresault = re.finditer(retag,atag,re.S)
            for item in fresault:
                songtag=item.group("stag") #歌曲标识
                sgname=item.group("sgname") #歌曲名称
                srname=item.group("srname") #歌手名称
                i = 0
                if ((sgname == sname) | (sgname == sname+srname) | (sgname == srname+sname)| (sgname.startswith(sname))) & (srname.startswith(ssrname)):
                   
                    #拼接歌曲下载地址
                    songurl="https://zz123.com/xplay/?act=songplay&id="+songtag
                    #检差歌曲文件夹是否存在
                    fname=op_avr.get().replace('/','\\')+'\\'+srname+'\\'+sname
                    folder = os.path.exists(fname)
                    if not folder:
                        os.makedirs(fname)
                    #读取歌曲
                    songres = requests.get(songurl,headers=headers,stream=True)
                    #获取文件地址
                    singname= sgname+".mp3" #歌曲保持名称.mp3s
                    file_path = os.path.join(fname,singname) #歌曲保存路径
                    dl_res.insert('end',"开始写入文件"+file_path+"\n")
                    dl_res.update()#刷新文本框显示
                    
                    #打开本地路径以二进制的方式写入文件，保存到文件夹
                    with open(file_path,'wb') as fd:
                        for chunk in songres.iter_content():
                            fd.write(chunk)
                    dl_res.insert('end',sname+"成功下载"+"\n")
                    dl_res.update()#刷新文本框显示
                    fd.close()
            
                    #获取歌词下载地址        
                    lrcurl = "https://zz123.com/geci/"+songtag+".htm"
                    lrcweb = requests.get(lrcurl,headers).text 
                    lrccontent = BeautifulSoup(lrcweb,"html.parser")
                    lrcres =str(lrccontent.find('div',attrs={'class':'lyric-block'}))
                    relrc = r'data-clipboard-text="(?P<lrc>.*?)">'
                    lrc = re.finditer(relrc,lrcres,re.S)
                    i = 0
                    for lr in lrc:
                        lrctxt = lr.group("lrc") 
                        if i==0:
                            lrc_path =os.path.join(fname,sgname+".txt")                
                        else:
                            lrc_path =os.path.join(fname,sgname+".lrc")
                        fb = open(lrc_path,mode='w',encoding='utf-8')
                        fb.write(lrctxt)
                        i = i+1
                        fb.close()   
                        dl_res.insert('end',sgname+'歌词下载完成' +"\n")
                        dl_res.update()#刷新文本框显示
                        break                
                                    
                    break
                else:
                    continue   
            if i == 0 :
                dl_res.insert('end',"搜到歌曲但无名为《"+sname+"》的歌曲" +"\n")
                dl_res.update()#刷新文本框显示
                with open("下载失败的歌曲.txt","a") as file:
                    file.write(sname)
                    file.write("\n")
                file.close()
        else:        
            dl_res.insert('end',"没有搜到名为《"+sname+"》的歌曲" +"\n")
            dl_res.update()#刷新文本框显示
            with open("下载失败的歌曲.txt","a") as file:
                file.write(sname)
                file.write("\n")
            file.close()    



     
    ##################################################################################
    t1 = text_songname.get()  # 获取文本输入框的内容
    if (t1 != '') | (fl_entry.get() != ''):
        if  fl_entry.get() == '' :# 判断是否文件下载为空，如果是空，可以直接下载输入的歌曲
        #获取需要搜索的歌曲
            longname = t1
            sname = longname.split(' ')[0]   # 使用空格分割字符串，空格后的字符是歌手名用于确定歌曲
            dl_res.insert('end',"#######################################################################\n")
            dl_res.update()#刷新文本框显示
            dl_res.insert('end',"正在搜索歌曲《"+sname+"》，请稍后...\n")
            dl_res.update()#刷新文本框显示
            if longname != sname:
        
                ssrname =longname.split(' ')[1]
                #dl_res.insert('end',sname+"singer"+ssrname+"\n") 打印歌手和歌曲名
                mp3download(op_avr,sname, ssrname)
            else:
                # dl_res.insert('0.0',sname+"\n") 打印歌曲名
        
                mp3download(op_avr,sname)
        elif t1 == '':
           dl_res.insert('end',"#######################################################################\n")
           dl_res.update()#刷新文本框显示
           dl_res.insert('end',"从文件开始下载歌曲\n")
           dl_res.update()#刷新文本框显示
           dl_res.insert('end',"读取文件中请稍后...\n")
           dl_res.update()#刷新文本框显示
           dl_res.insert('end',"读取文件中请稍后......\n")
           dl_res.update()#刷新文本框显示
           
           #输入需要请求的关键词
           songs=open(fl_entry.get(),'r',encoding='utf-8')
           ssgs=songs.readlines()
           dl_res.insert('end',"读取成功！\n")
           dl_res.update()#刷新文本框显示
           cc = 1
           for song in ssgs:
             longname = song.strip()  #分割每首歌
             sname = longname.split(' ')[0]   # 使用空格分割字符串，空格后的字符是歌手名用于确定歌曲
             if longname != sname:
                 ssrname =longname.split(' ')[1]
                 mp3listdownload(op_avr,sname,cc,ssrname)
             else:
                 mp3listdownload(op_avr,sname,cc) 
             cc= cc + 1     
           songs.close() 
           dl_res.insert('end',"所有歌曲下载完成\n")
           dl_res.update()#刷新文本框显示
        else:
            dl_res.insert('end',"不能同时输入歌曲和歌曲文件，请删除一个后重试！\n")
            dl_res.update()#刷新文本框显示
        
    else:
        dl_res.insert('end',"请输入要下载的歌曲，或者浏览以选择要下载的歌曲单文件\n")
        dl_res.update()#刷新文本框显示

###############################################################################
####################################创建MP3界面#################################
mp3 = tk.Tk()  #
mp3.title("Falloon`s MP3downloader") # 设置窗口标题
mp3.geometry('800x600') # 设置界面像素大小

###############################################################################
##################################运行过程显示框################################
dl_res = tk.Text(mp3,height='30',width='110')
dl_res.place(x=10,y=150, anchor='nw')
dl_res.delete('0.0','end')  #删除文本框的内容 
###############################################################################

####################################输入框定义##################################
#添加标签和输入框
lable_songname = tk.Label(mp3,text="请输入要下载的音乐名称：") #输入框前面的说明文字
lable_songname.place(x=10,y=20,anchor='nw') # 靠左，上部
text_songname = tk.Entry(mp3,width='35') #添加输入框并定位到顶部靠左，接着上一个
text_songname.place(x=160,y=20,anchor='nw')
lable_songname = tk.Label(mp3,text="（音乐名称 或 音乐名称+空格+歌手 ）") #输入框后面的说明文字
lable_songname.place(x=450,y=20,anchor='nw') #输入框后面的说明文字的位置

############################从文件下载歌曲，或清除文件信息返回歌词下载内容
#浏览文件功能

lable_path = tk.Label(mp3,text='请选择要下载的音乐名列表的路径:').place(x=10,y=70,anchor='nw')
lable_phlb = tk.Label(mp3,text='（文件要求为：歌名或歌名+空格+歌手，每行一首歌的txt文件）').place(x=10,y=90,anchor='nw')
path_avr = tk.StringVar()
fl_entry = tk.Entry(mp3,textvariable=path_avr)
fl_entry.place(x=200,y=70,width='200',anchor='nw')


but_ep = tk.Button(mp3,text="浏览",command=scan).place(x=480,y=62,anchor='ne') #引用scan子程序
#返回文件的按钮
but_ep = tk.Button(mp3,text="清除文件",command=d_scan).place(x=560,y=62,anchor='ne') #引用d_scan子程序

###############################################################################

##################################输出文件夹位置################################
lable_path = tk.Label(mp3,text='请选择下载路径:').place(x=10,y=120,anchor='nw')
lable_phlb = tk.Label(mp3,text='（路径为空则表示下载在软件所在文件夹）').place(x=570,y=120,anchor='nw')
op_avr = tk.StringVar()
dl_out = tk.Entry(mp3,textvariable=op_avr)
dl_out.place(x=200,y=120,width='200',anchor='nw')
but_so = tk.Button(mp3,text="浏览",command=oscan).place(x=480,y=112,anchor='ne') #引用scan子程序
#返回文件的按钮
but_do = tk.Button(mp3,text="清除路径",command=do_scan).place(x=560,y=112,anchor='ne') #引用d_scan子程序

###############################################################################

#添加下载功能按钮 

but_dl= tk.Button(mp3,text="下载音乐",command=mp3_dl) #利用tk创建按钮名为下载音乐
but_dl.place(x=380,y=560,anchor='n') #添加到窗口中位置默认是上部居中pack(side='top’,anchor='center’)

#窗体循环要在所有控件创建完毕后循环，否则无法加载循环开始后的控件。
mp3.mainloop() #启动窗口时间循环 
