try:
    import webbrowser,threading,sys,tkinter as tk,wget,logging,os,time,random as rd,requests,pandas as pd
    from PIL import Image, ImageDraw, ImageFont, ImageTk
    from tkinter import ttk
    from tkinter.messagebox import showerror, showinfo
except:
    print("环境验证失败")
    try:
        import os
    except:
        print("请安装os后继续，否则我们将会无法自动安装")
        input()
        os._exit(1)
    else:
        get_input = input("是否自动尝试安装环境？y/n :")
        if get_input == "y" or get_input == "Y" or get_input == "yes" or get_input == "Yes" or get_input == "YEs" or get_input == "YES" :
            print("正在自动安装环境")
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            try:
                if "requirements.txt" in os.listdir(os.path.dirname(os.path.abspath(__file__))):
                    os.system("pip install -r requirements.txt")
                else:
                    print ("无法检测到requirements.txt")
                    os.system("pip install wget requests pandas pillow")

            except:

                print("环境由于未知原因安装失败，请手动安装")
                input()
                os._exit(1)
            else:
                try:
                    import webbrowser,threading,sys,tkinter as tk,wget,logging,os,time,random as rd,requests,pandas as pd
                    from PIL import Image, ImageDraw, ImageFont, ImageTk
                    from tkinter import ttk
                    from tkinter.messagebox import showerror, showinfo
                except:
                    print("安装失败，请手动安装")
                    input()
                    os._exit(1)
                else:
                    os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    print("环境验证完成")
                    if "Idiom_in_tk.py" in os.listdir(os.path.dirname(os.path.abspath(__file__))):

                        os.system("python.exe Idiom_in_tk.py")
                    else:
                        print("无法检测到文件")
                    print("程序结束")
                    print("后续可直接使用 Idiom_in_tk.py 启动程序")
                    input()
                    os._exit(0)
        else:
            print("即将退出")
            input()
            os._exit(0)
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("环境验证完成,一切正常！")
    if "Idiom_in_tk.py" in os.listdir(os.path.dirname(os.path.abspath(__file__))):

        os.system("python.exe Idiom_in_tk.py")
    else:
        print("无法检测到文件,请注意是否缺少主程序？\n即将退出")
        input()
        os._exit(0)
    print("程序结束")
    print("后续可直接使用 Idiom_in_tk.py 启动程序")
    input()
    os._exit(0)