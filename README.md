# Idiom solitaire
 借助于idiom-database再次开发的成语接龙软件
 程序使用了"得意黑"字体

## 功能
- 成语接龙
- 成语查询
- 游戏教学

## 需要注意的点:
- 成语接龙时,需要遵守成语接龙的规则,即接上来的成语的第一个字的读音要和上一个成语的最后一个字的读音相同
- 该成语接龙程序中所提到的成语不仅限于四字成语,还包括八字等
- 成语库不太全,有些成语识别不上来
- 因为程序算法,有时候会卡住,关闭程序即可
- 成语接龙分为三个版本
    - terminal 版本
    - tk 版本
    - 建议运行tk版本,有图形化界面
- 该程序是开源的,使用GPL-3.0协议,可以随意修改,但必须保留原作者信息

## 文件相关
- 成语接龙.py/成语接龙_tk.py 是主程序 有tk后缀的是图形化界面版本
- idiom.csv是必不可少的依赖文件,主要的程序都是基于他的
- cyjl.log是程序的log
- empty_zhengshu.jpg 是生成证书相关文件

## 使用开源仓库
- https://github.com/atelier-anchor/smiley-sans LICENSE:SmileySans-Oblique_LICENSE.txt
- https://github.com/crazywhalecc/idiom-database  LICENSE:idiom_LICENSE.txt 

## 安装
- 下载.exe格式的文件无需安装,程序会自动安装所需文件
- 下载 zip/7zip 格式的文件需要安装,下载后解压到任意位置,运行主程序即可
- 下载.py格式的文件需要安装python环境(见运行环境),下载后运行主程序即可,程序会自动安装其他所需文件

## 运行环境
- .exe 无需配置,直接运行即可
- 针对于.py格式的文件
    - 请下载python 3.X 环境
    - 请下载以下几个库
        - webbrowser
        - threading
        - tkinter
        - wget
        - logging
        - os
        - time
        - random
        - requests
        - pandas
        - pillow
