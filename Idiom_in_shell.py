import pandas as pd
import requests
import random as rd
import time
from PIL import Image, ImageDraw, ImageFont
import os
import logging
import wget
logging.basicConfig(level=logging.DEBUG, filename="cyjl.log")
logging.warning('-----------------------------程序开始/启动-----------------------------')
logging.info('程序:成语接龙 版本:控制台1.0 乐乐出品')
short=True
nameglobal=''
def download_csv(url):
    global download
    download=False
    filename = "idiom.csv"
    if not os.path.isfile(filename):
        logging.info("开始下载csv")
        print("正在下载必要文件")
        # urllib.request.urlretrieve(url, filename)
        wget.download(url, filename)
        logging.info("下载csv成功")
        download=True
    else:
        logging.info("无需下载csv")
    #返回csv
    
    return open(filename)
#函数： 从url下载照片，并返回
def download_image(url):

    #从url下载照片，把照片存成文件名"empty_zhengshu.jpg"
    filename = "empty_zhengshu.jpg"

    if not os.path.isfile(filename):
        logging.info("开始安装图片原图")
        print("正在下载图片")
        wget.download(url, filename)
        logging.info("图片原图调用完成")
    #读取照片
    img = Image.open(filename)
    logging.info("读取图片完成")

    #返回照片
    logging.info("返回图片中")
    return img

#函数： 从url下载字体，并返回
def download_font(url, font_size):

    #下载字体，并把字体存成文件名："SmileySans-Oblique.ttf"
    filename = "SmileySans-Oblique.ttf"
    if not os.path.isfile(filename):
        logging.info("开始下载字体")
        print('正在下载字体')
        wget.download(url, filename)
        logging.info("字体下载完成!")
    #读取字体，并设置字体的大小
    font = ImageFont.truetype(filename, font_size)
    logging.info("读取图片完成")
    #返回字体
    logging.info("返回字体")
    return font

#函数： 在图片上写中文
def draw_text(image_url, text, font_url):

    #设置字体颜色，位置，大小
    text_color = (0,0,0)
    position = (741, 99)
    font_size = 180
    logging.info("draw_text:颜色,位置,字体大小设置完毕")
    #读取图片和字体
    img = download_image(image_url)
    font = download_font(font_url, font_size)
    logging.info("函数正常调用")
    #开始写字
    logging.info("开始写字")
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=text_color)
    logging.info("写字完成个")
    img.save("zhengshu.jpg")
    print('证书生成完成,3秒后展示')
    logging.info("输出:证书生成完成,3秒后展示")
    print("点击『输入键』继续")
    logging.info("输入:提示用户点击输入键继续")
    logging.info("开始停止3秒")
    time.sleep(3)
    logging.info("停止3秒完成")
    img.show()
    logging.info("展示完成")
def mainif(name,input):
    logging.info("程序输出是:"+name)
    logging.info("输入是:"+input)
    if input in csv_word_list:
        input_index=csv_word_list.index(input)
        name_index=csv_word_list.index(name)
        input_pinyin = csv['pinyin'][input_index].split()
        name_pinyin = csv['pinyin'][name_index].split()
        if input_pinyin[0]==name_pinyin[len(name_pinyin)-1]:
            logging.info("用户输入正确")
            return '成功!'
            
        else:
            print('回答不正确')
            logging.info("用户输入不合规")
            return '失败'
    else:
        print('没有这个成语!')
        logging.info("用户输入没有此成语")
        return '失败'
print('本程序使用了idiom-database开源库,在此表示感谢')
image_url='http://code.files.lawrenceshi.space/idiom-database-master/data/img.jpg'
csv_url = 'http://code.files.lawrenceshi.space/idiom-database-master/data/idiom.csv'
font_url='http://code.files.lawrenceshi.space/idiom-database-master/data/SmileySans-Oblique.ttf'
ifzhengshu=False
#csv_url='L:\乐乐\乐乐编程\乐乐python\成语接龙.csv'
logging.info("调用函数'下载csv'开始!")
csv=download_csv(csv_url)
csv = pd.read_csv(os.getcwd()+'\idiom.csv',encoding='utf-8')
csv_word_list=[]
csv_pingyin_list=[]
for i in csv['word']:
    csv_word_list.append(i)
for i in csv['word']:
    csv_word_list.append(i)
loap=0
new=csv['word'][rd.randint(0,len(csv)-1)]
while True:
    #new='十全十美'
    logging.info("程序输出")
    if download and loap==0:
        print('\n请听题!'+new)
    else:
        print('请听题!'+new)
    time.sleep(0.5)
    name=input('你出什么?')
    nameglobal=name
    if mainif(new,name) == '成功!':
        time.sleep(0.5)
        print('太厉害了!')
        loap+=1
    else:
        time.sleep(0.5)
        print('你太弱了!!!')
        break
    if loap>=15:
        logging.info("大于程序退出次数!")
        print('我在想一想...')
        print('(请等待程序思考*^_^*)')
        time.sleep(3)
        print('我好像打不出来了...算你赢吧')
        logging.info("程序认输!")
        if input('是否生成证书（y/n）')=='y':
            logging.info("用户要生成证书")
            print('正在生成...')
            #证书生成程序由爸爸提供并编写
            #===========
            #以下是主程序
            #===========
            # 这里是你要写的字
            text = input('请输入你的名字(用于输出证书):')
            # 写字
            print('调用文件可能需要一段时间')
            ifzhengshu=True
            draw_text(image_url, text, font_url)
        break
    
    while True:
        logging.info("开始循环输出新的成语")
        new=csv['word'][rd.randint(0,len(csv)-1)]
        name_index=csv_word_list.index(nameglobal)
        new_index=csv_word_list.index(new)
        name_pinyin = csv['pinyin'][name_index].split()
        new_pinyin = csv['pinyin'][new_index].split()
        if new_pinyin[0]==name_pinyin[len(name_pinyin)-1]:
             logging.info("成语合规!为:"+new)
             break
        else:
            logging.info("成语不合规!为:"+new)
logging.info("询问是否删除文件")
if short:
    if input('是否保留文件(不包含:证书(如果已经生成),日志!)(y/n):') == 'n':
        logging.warning("要求删除文件")
        if ifzhengshu:
            os.remove('empty_zhengshu.jpg')
            os.remove('SmileySans-Oblique.ttf')
            logging.info("证书相关删除完毕")
        os.remove('idiom.csv')
        print('日志请手动清除')
        logging.warning("所有文件删除完毕")
        print('已经成功删除!')
    else:
        print('我们将保留数据')
        logging.info("用户要求保留文件")
print('你一共答对了'+str(loap)+'次!')
logging.info("用户答对了:"+str(loap)+'次!')
logging.info("关闭程序循环开始")
for i in range(15,0,-1):
    logging.info("还有"+str(i)+'秒后关闭程序')
    print('我们将会在'+str(i)+'秒后自动关闭程序,你也可以点击叉号关闭')
    time.sleep(1)
logging.warning("-----------------------------程序关闭-----------------------------")

# print(csv)
