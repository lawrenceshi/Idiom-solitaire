import webbrowser,threading,sys,tkinter as tk,wget,logging,os,time,random as rd,requests,pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
#设置logging
def createLogger(filename="cyjl.log"):

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename, mode='w')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.INFO)
    
    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s --- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s\n', datefmt='%Y-%m-%d %H:%M:%S')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


#主要的class
class App(tk.Tk):

    def __init__(self):

        global logger

        #设置ifjielong变量，还原里要用到
        self.ifjielong=False
        self.tips=0

        #初始化
        super().__init__()
        logger.info('class初始化')

        #set title/geomety/resizable
        #设置界面的标题/大小/是否可以伸缩
        self.title('成语接龙')
        self.geometry('500x225')
        self.resizable(False,False)
        logger.info("界面标题/大小/是否可伸缩")

        #set style
        #设置style
        self.style = ttk.Style()
        self.style.configure('My.TLabel', anchor=tk.CENTER)
        logger.info("style设置完成")

        #以下是下载进度条的代码

        #创建一个提示等待下载完毕的label
        info_label_3=ttk.Label(self,text="请等待下载完成")
        logger.info("提示等待下载完成label创建完成")
        info_label_3.grid(row=1,column=1,columnspan=2,sticky=tk.EW)
        #创建url变量
        self.csv_url = 'http://code.files.lawrenceshi.space/idiom-database-master/data/idiom.csv'
        logger.info("url变量创建完成")

        #如果csv文件不存在
        if not os.path.isfile("idiom.csv"):
            logger.info('csv文件不存在,开始下载')
            #创建下载的指定窗口
            downloadTop = DownloadWgetTop(self,self.csv_url, "idiom.csv")
            #见class设置

            #set title/geomety/resizable/
            #设置界面的标题/是否可以伸缩/显示位置
            downloadTop.resizable(False, False)
            x, y = self.winfo_x(), self.winfo_y()
            downloadTop.geometry("+%d+%d" %(x+100,y+100))
            downloadTop.grab_set()

            #mainloop
            downloadTop.mainloop()

        #删除提示下载标签
        info_label_3.destroy()

        #set variable
        #一些变量的创建
        self.loop=0
        self.image_url='http://code.files.lawrenceshi.space/idiom-database-master/data/img.jpg'
        self.font_url='http://code.files.lawrenceshi.space/idiom-database-master/data/SmileySans-Oblique.ttf'
        self.csv = pd.read_csv(os.getcwd()+'\idiom.csv',encoding='utf-8')
        self.csv_word_list=self.csv['word'].tolist()
        self.csv_pinyin_list=self.csv['pinyin'].tolist()
        self.csv_derivation_list=self.csv['derivation'].tolist()
        self.csv_example_list=self.csv['example'].tolist()

        #底部菜单/欢迎菜单创建
        self.welcome_widget()
        self.bottom_widget()
        
        logger.info("界面创建完成")

    #欢迎界面
    def welcome_widget(self):
        self.new_label=ttk.Label(self, text = "欢迎来到乐乐成语接龙:", style='My.TLabel')
        self.new_label.grid(row = 0, column = 0, columnspan=4 ,padx = 5, pady = 5, sticky=tk.EW)

        self.start_button=ttk.Button(self, text='开始接龙', command=self.after_start)
        self.start_button.grid(row = 1, column = 1,  padx = 5, pady = 5, sticky=tk.EW)

        logger.info("欢迎界面创建完成")
    #函数： 从url下载照片，并返回
    def download_image(self,url):

        #从url下载照片，把照片存成文件名"empty_zhengshu.jpg"
        filename = "empty_zhengshu.jpg"

        if not os.path.isfile(filename):
            logger.info("开始安装图片原图")
            print("正在下载图片")
            wget.download(url, filename)
            logger.info("图片原图调用完成")
        #读取照片
        img = Image.open(filename)
        logger.info("读取图片完成")

        #返回照片
        logger.info("返回图片中")
        return img

    #底部菜单创建
    def bottom_widget(self):

        self.copyright_label=ttk.Label(self, text = "©2023 乐乐成语接龙 Lawrence Shi/Hao Shi")
        self.copyright_label.grid(row = 3, column =0, padx = 5, pady = 5, sticky=tk.EW)
        
        self.huanyuan_button=ttk.Button(self, text='还原＆重置', command=self.after_huanyuan)
        self.huanyuan_button.grid(row = 3, column = 1, padx = 5, pady = 5, sticky=tk.W)

        self.close_button=ttk.Button(self, text='关闭', command=self.after_close)
        self.close_button.grid(row = 3, column = 2, padx = 5, pady = 5, sticky=tk.W)

        open_button = tk.Button(self, text="BLOG", command=lambda: webbrowser.open("http://lawrenceshi.space"))
        open_button.grid(row = 4, column = 1, padx = 5, pady = 5, sticky=tk.EW)

        github_button = tk.Button(self, text="Github", command=lambda: webbrowser.open("https://github.com/lawrenceshi"))
        github_button.grid(row = 4, column = 2, padx = 5, pady = 5, sticky=tk.EW)

        logger.info("欢迎界面底部创建完成")

    #开始函数
    def after_start(self):

        logger.info("用户点击'开始'按钮")

        #删除欢迎界面的标签和按钮
        self.new_label.destroy()
        self.start_button.destroy()
        logger.info("欢迎界面/按钮销毁完成")

        #生成接龙标签
        self.start_jielong()

    def start_jielong(self):
        #用于重置的变量
        self.ifjielong=True
        self.new=self.csv['word'][rd.randint(0,len(self.csv)-1)]
        logger.info("开始接龙!")
        self.info_label_1=ttk.Label(self, text = "程序出:")
        self.info_label_1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=tk.E)

        self.new_label=ttk.Label(self, text = self.new, style='my.TLabel')
        self.new_label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=tk.EW)

        self.info_label_2=ttk.Label(self, text = "请输入:")
        self.info_label_2.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=tk.E)

        self.chengyu_entry = ttk.Entry(self, width=15,)
        self.bind("<Return>", self.after_submit)
        self.chengyu_entry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky=tk.E)

        self.submit_button = ttk.Button(self, text='提交', command=self.after_submit)   
        self.submit_button.grid(row = 1, column =2, padx = 5, pady = 5, sticky=tk.E)

        self.loop_button = ttk.Button(self, text='次数', command=self.after_loop)
        self.loop_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.example_button = ttk.Button(self, text='程序出的成语的 拼音/事例/来处', command=self.after_example)
        self.example_button.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        self.tip_button= ttk.Button(self, text='提示', command=self.after_tip)
        self.tip_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

        logger.info("接龙界面/按钮创建完成")

    #提示
    def after_tip(self):

        #持续循环
        while True:
            new=self.csv['word'][rd.randint(0,len(self.csv)-1)]
            if self.mainif(self.new,new):
                logger.info('循环结束')
                break
        
        #得出来的index
        new_index = self.csv_word_list.index(new)


        #显示
        showinfo( title="提示", message="可以出:"+new+"\n"+"拼音:"+ self.csv_pinyin_list[new_index]+'\n来处:'+self.csv_derivation_list[new_index]+'\n实例:'+self.csv_example_list[new_index])
        logger.info("提示弹窗完成")

        #增加提示次数
        self.tips+=1
        logger.info("提示次数:"+str(self.tips))

    def after_example(self):
        logger.info("用户点击了具体事例/来处按钮")
        new_index = self.csv_word_list.index(self.new)
        showinfo( title="提示", message="具体事例: "+ self.csv_example_list[new_index] +"\n来处: "+ self.csv_derivation_list[new_index]+"\n"+"拼音:"+ self.csv_pinyin_list[new_index])
        logger.info("提示弹窗完成")

    def after_loop(self):
        logger.info("用户点击'次数'按钮")
        if self.loop==0:
            showinfo( title="提示", message="你还没有回答过")
        else:
            showinfo( title="提示", message="你已经回答了"+str(self.loop)+"次\n提示了"+str(self.tips)+"次\n您的提示率为:"+ str(self.tips/self.loop*100) + "%\n温馨提醒:只有无提示才能获得证书")
        logger.info("提示弹窗完成")

    def after_huanyuan(self):
    
        logger.warning("用户点击还原/重置按钮重启了程序")

        #如果开启了接龙
        if self.ifjielong:
            # 销毁一些标签
            self.info_label_1.destroy()
            self.new_label.destroy()
            self.info_label_2.destroy()
            self.chengyu_entry.destroy()
            self.submit_button.destroy()
            self.loop_button.destroy()
            self.example_button.destroy()
            self.tip_button.destroy()
            logger.info("接龙界面/按钮销毁完成")

            #重置变量
            self.ifjielong=False
            self.loop=0
            self.tips=0

            #重新生成欢迎界面
            self.welcome_widget()

        else:

            #如果没有开始接龙
            showinfo( title="提示", message="您还没有开始接龙,无需重置")

    def after_submit(self,event=None):
        self.name=self.chengyu_entry.get()
        if self.mainif(self.new,self.name):

            #回答次数+1
            self.loop+=1

            #清空输入框
            self.chengyu_entry.delete(0,tk.END)

            #如果达到通关次数
            if self.loop>=10 and self.tips==0:

                logger.info("用户回答了10次,达到通关条件")

                #生成一个新弹窗
                self.zhengshu=tk.Toplevel()
                self.zhengshu.title("结算界面")

                #创建新弹窗的标签
                self.zhengshunew_label=ttk.Label(self.zhengshu, text = "程序想不出来了,算你赢qwq")
                self.zhengshunew_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=tk.E)

                self.zhengshuinfo_label=ttk.Label(self.zhengshu, text = "是否要生成证书呢?")
                self.zhengshuinfo_label.grid(row = 1, column = 2, padx = 5, pady = 5, sticky=tk.E)
                
                self.zhengshuinfo_label_2=ttk.Label(self.zhengshu, text = "请输入名字以便生成证书:")
                self.zhengshuinfo_label_2.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

                self.name_entry = ttk.Entry(self.zhengshu)
                self.name_entry.grid(row = 2, column = 2, padx = 5, pady = 5, sticky=tk.EW)

                self.zhengshuinfo_label=ttk.Label(self.zhengshu, text = '生成证书后自动结束程序')
                self.zhengshuinfo_label.grid(row = 3, column = 1, padx = 5, pady =5,sticky=tk.EW)

                self.zhengshu_button=ttk.Button(self.zhengshu, text = "不生成", command = self.after_close)
                self.zhengshu_button.grid(row = 3, column = 3, padx = 5, pady = 5, sticky=tk.E)

                self.zhengshu_button=ttk.Button(self.zhengshu, text = "生成", command = self.shengchengzhengshu)
                self.zhengshu_button.grid(row = 3, column = 2, padx = 5, pady = 5, sticky=tk.E)
                
                #mainloop
                self.zhengshu.mainloop()
                logger.info("生成证书新弹窗生成完成")

                #还原到主界面
                self.after_huanyuan()
            elif self.loop>=10 and self.tips!=0:
                showinfo( title="提示", message="不提示才能获得证书!")
                self.after_huanyuan()
            #提示答对了
            showinfo( title="提示", message="恭喜你，答对啦，请听下一题!")

            logger.info("开始循环输出新的成语")

            #生成新的new
            while True:
                self.new=self.csv['word'][rd.randint(0,len(self.csv)-1)]
                if self.mainif(self.name,self.new):
                    logger.info('循环结束')
                    break

            #更新标签
            self.new_label.configure(text = self.new)

            # 这是旧版程序
            # while True:
            #     logger.info("开始循环输出新的成语")
            #     self.new=self.csv['word'][rd.randint(0,len(self.csv)-1)]
            #     name_index=self.csv_word_list.index(self.name)
            #     new_index=self.csv_word_list.index(self.new)
            #     name_pinyin = self.csv['pinyin'][name_index].split()
            #     new_pinyin = self.csv['pinyin'][new_index].split()
            #     if new_pinyin[0]==name_pinyin[len(name_pinyin)-1]
            #         logger.info("成语合规!为:"+self.new)
            #         break
            #     else:
            #         logger.info("成语不合规!为:"+self.new)
            #     self.new_label.config(text='程序出:'+self.new)
            #     logger.info('显示新的成语')

        #否则(用户回答错误)
        else:

            logger.info("用户回答错误")

            #显示错误信息
            showerror( title="错误", message="对不起, 回答错误,请下次继续努力!")

            #重置标签
            self.after_huanyuan()
    
    #生成证书代码
    def shengchengzhengshu(self):

        logger.info("用户要生成证书")

        #证书生成程序由爸爸提供并编写
        #===========
        #以下是主程序
        #===========

        # 这里是你要写的字
        text = self.name_entry.get()

        # 写字/调用程序
        self.draw_text(self.image_url,text,self.font_url)

    #关闭程序
    def after_close(self):
        logger.warning("用户点击退出按钮关闭了程序")
        logger.warning("-----------------------------程序关闭-----------------------------")
        #关闭class
        self.destroy()
    
    #下载字体程序
    def download_font(self,url, font_size=180):
        #下载字体，并把字体存成文件名："SmileySans-Oblique.ttf"
        filename = "SmileySans-Oblique.ttf"
        if not os.path.isfile(filename):
            logger.info("开始下载字体")
            print('正在下载字体')
            wget.download(url, filename)
            logger.info("字体下载完成!")
        #读取字体，并设置字体的大小
        font = ImageFont.truetype(filename, font_size)
        logger.info("读取图片完成")
        #返回字体
        logger.info("返回字体")
        return font

    #下载文件
    def download_file(self,url,filename):
        #让download全局
        global download
        #定义
        download=False

        #如果没有文件
        if not os.path.isfile(filename):
            #下载
            logger.info("开始"+filename+"的下载")
            print("正在下载必要文件")
            wget.download(url, filename)
            logger.info("下载"+filename)
            download=True
        else:
            #log
            logger.info("无需下载")

    #绘制文件
    def draw_text(self,image_url, text, font_url):

        #设置字体颜色，位置，大小
        text_color = (0,0,0)
        position = (741, 99)
        font_size = 180
        #读取图片和字体
        img = self.download_image(image_url)
        font = self.download_font(font_url, font_size)
        #开始写字
        draw = ImageDraw.Draw(img)
        draw.text(position, text, font=font, fill=text_color)

        #把图片存起来
        img.save("zhengshu.jpg")
        logger.info("图片保存完成")

        #展示图片
        img.show()

        #关闭程序
        self.after_close()

    #主判断程序
    def mainif(self,name,input):

        #如果程序在数据库里
        if input in self.csv_word_list:

            #生成变量
            input_index=self.csv_word_list.index(input)
            name_index=self.csv_word_list.index(name)
            input_pinyin = self.csv['pinyin'][input_index].split()
            name_pinyin = self.csv['pinyin'][name_index].split()

            #判断
            if input_pinyin[0]==name_pinyin[len(name_pinyin)-1]:
                logger.info("输出 正确")
                return True
                
            else:
                return False
        else:
            logger.info("输入没有此成语")
            return False

#下载文件进度条
class DownloadWgetTop(tk.Toplevel):
  
    def __init__(self, container, url, filename):
        
        global logger

        #Initial
        #初始化
        super().__init__(container)
        logger.info("DownloadWgetTop初始化完成")

        #Initial variables
        #设置一些变量
        self.url = url
        self.filename = filename
        logger.info("DownloadWgetTop创建变量完成")

        #Set info
        #设置窗口大小/标题
        self.geometry( '320x120' )
        self.title('下载中')
        logger.info("DownloadWgetTop设置窗口大小/标题完成")

        #Create widgets
        #创建界面
        #见def __create_widgets()
        self.__create_widgets()

        #Start the download, use threading method
        download_thread = threading.Thread(target=self.__download)
        download_thread.start()


    def __create_widgets(self):
        
        #创建界面
        download_label = ttk.Label( self, text= "正在下载文件 {}".format(self.filename) )
        download_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky='NS')

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=310, mode="determinate")
        self.progress_bar.grid(row = 1, column = 0, padx = 5, pady = 15, sticky='NESW')

        self.precent_label = ttk.Label(self, text= "0%")
        self.precent_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky='NS')

        logger.info("DownloadWgetTop创建界面完成")

    #Download by wget
    #通过wget库下载文件
    def __download(self):
        logger.info("进入下载函数")
        #bar是指进度条
        wget.download(self.url, self.filename, bar= self.__update_progress_bar)
        logger.info("下载完成")
        #退出mainloop/关闭窗口
        self.quit()
        self.destroy()
        #见def __update_progress_bar
    
    #Update the progressbar
    #更新进度条函数
    def __update_progress_bar(self, current, total, width=80):
        logger.info("进入进度条函数")
        #计算 '已下载的字符数'/(除以)'总共的字符数' *(乘以) 100 得到百分比
        percentage = int( (current/total) * 100 )

        #更新进度条/进度条底下的文本
        self.progress_bar.config( value=current, maximum=total )
        self.precent_label.config( text="{}%".format(percentage) )

        #如果下载完成
        if current == total:
            logger.info('进度条函数检测下载完成给')

            #更新文本
            self.precent_label.config( text="100% - 下载完成" )


if __name__ == "__main__":
        
    #创建logger
    logger = createLogger(filename="cyjl.log")
    logger.warning('-----------------------------程序开始/启动-----------------------------')
    logger.info('成语接龙tk版本 1.1')
    logger.info('Copyright 2023-'+str(time.strftime("%Y"))+' 乐乐成语接龙 Lawrence Shi(Github:lawrenceshi bilibili:喜欢探究的乐乐)/Hao Shi(Github:hshi)')

    #mainloap
    app = App() 
    logger.info("程序进入mainloop")
    app.mainloop()
