from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk 

import shapefile
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.collections import PolyCollection
from matplotlib.patches import Circle
from matplotlib.cm import get_cmap

import os

def resource_path(relative_path):
    """定义一个读取相对路径的函数"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class EvaluationSystem(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root

        self.allResults = []

        self.resImgSrc = "./test.png"
        self.firstDraw = True
        self.figNum = 0

        self.levelMap = {
            '恶劣': (1, 0, 1, 1),
            '差': (1, 0, 0, 1),
            '中': (1, 0.5, 0, 1),
            '良': (1, 1, 0, 1),
            '优': (0, 1, 0, 1)
        }

        self.regionMap = {
            '香洲': {id: 'G3800', 'longitude': '113.5667', 'latitude': '22.275'},
            '保税区': {id: 'G3850', 'longitude': '113.4943', 'latitude': '22.1769'},
            '翠微': {id: 'G3852', 'longitude': '113.5112', 'latitude': '22.2661'},
            '界涌': {id: 'G3853', 'longitude': '113.4934', 'latitude': '22.3174'},
            '珠海港': {id: 'G3856', 'longitude': '113.184', 'latitude': '21.97'},
            '斗门镇': {id: 'G3858', 'longitude': '113.183', 'latitude': '22.233'},
            '香洲港': {id: 'G3859', 'longitude': '113.579', 'latitude': '22.292'},
            '香灶镇': {id: 'G3860', 'longitude': '113.348', 'latitude': '22.049'},
            '高栏西': {id: 'G3862', 'longitude': '113.227', 'latitude': '21.928'},
            '湾仔': {id: 'G1221', 'longitude': '113.525', 'latitude': '22.204'},
            '横琴桥': {id: 'G1226', 'longitude': '113.513', 'latitude': '22.163'},
            '淇澳桥': {id: 'G1227', 'longitude': '113.611', 'latitude': '22.388'},
            '情侣北': {id: 'G1229', 'longitude': '113.616', 'latitude': '22.35'},
            '保税区新站': {id: 'G1230', 'longitude': '113.4943', 'latitude': '22.1769'},
            '港珠澳大桥': {id: 'G1231', 'longitude': '113.6407', 'latitude': '22.2461'},
            '井岸': {id: 'G1250', 'longitude': '113.283', 'latitude': '22.217'},
            '灯笼': {id: 'G1252', 'longitude': '113.372', 'latitude': '22.203'},
            '新乡村': {id: 'G1253', 'longitude': '113.167', 'latitude': '22.26'},
            '大赤坎': {id: 'G1255', 'longitude': '113.235', 'latitude': '22.278'},
            '白藤大闸': {id: 'G1256', 'longitude': '113.362', 'latitude': '22.163'},
            '白藤湖': {id: 'G1258', 'longitude': '113.32', 'latitude': '22.188'},
            '白蕉': {id: 'G1259', 'longitude': '113.332', 'latitude': '22.258'},
            '竹洲': {id: 'G1262', 'longitude': '113.267', 'latitude': '22.367'},
            '斗门大桥': {id: 'G1265', 'longitude': '113.352', 'latitude': '22.27'}
        }

        self.initUI()

        

    def initUI(self):
        self.root.title("气象宜居指数计算系统")
        self.mainframe = ttk.Frame(self.root, padding="6 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        #文本与按钮部分
        ttk.Label(self.mainframe, text="区点").grid(column=2, row=1, sticky=W)
        ttk.Label(self.mainframe, text="月份").grid(column=2, row=2, sticky=W)
        ttk.Label(self.mainframe, text="月均气温(℃)").grid(column=2, row=3, sticky=W)
        ttk.Label(self.mainframe, text="月降水量(mm)").grid(column=2, row=4, sticky=W)
        ttk.Label(self.mainframe, text="月均AQI").grid(column=2, row=5, sticky=W)
        ttk.Label(self.mainframe, text="月均大气通风量(m2/s)").grid(column=2, row=8, sticky=W)
        ttk.Label(self.mainframe, text="月均湿度(%)").grid(column=2, row=6, sticky=W)
        ttk.Label(self.mainframe, text="月均地面风速(m/s)").grid(column=2, row=7, sticky=W)
        ttk.Label(self.mainframe, text="                 ").grid(column=4, row=3, sticky=W)
        ttk.Label(self.mainframe, text="指标").grid(column=5, row=2)
        ttk.Label(self.mainframe, text="气温").grid(column=5, row=3)
        ttk.Label(self.mainframe, text="降水量").grid(column=5, row=4)
        ttk.Label(self.mainframe, text="污染物浓度").grid(column=5, row=5)
        ttk.Label(self.mainframe, text="大气净化能力").grid(column=5, row=6)
        ttk.Label(self.mainframe, text="人体舒适度").grid(column=5, row=7)
        ttk.Label(self.mainframe, text="各项权重  ").grid(column=6, row=2)
        ttk.Label(self.mainframe, text="各项得分  ").grid(column=7, row=2)
        ttk.Label(self.mainframe, text="气象宜居指数得分").grid(column=8, row=7, sticky=W)
        ttk.Button(self.mainframe, text="计算", command=self.calculate).grid(column=3, row=9, sticky=W)

        self.btn = ttk.Button(self.mainframe, text='使用当月值', command=self.switchBtn1Status)
        self.btn.grid(column=4, row=8, sticky=W)

        #输入部分
        self.region = StringVar()
        self.month = StringVar()
        self.T = StringVar()
        self.R = StringVar()
        self.P = StringVar()
        self.J = StringVar()
        self.H = StringVar()
        self.V = StringVar()

        self.region_Chosen = ttk.Combobox(self.mainframe, width=9, textvariable=self.region)
        regions = [r for r in self.regionMap.keys()]
        self.region_Chosen['values'] = regions
        self.region_Chosen.grid(column=3, row=1)
        self.region_Chosen.current(1)

        self.month_Chosen = ttk.Combobox(self.mainframe, width=9, textvariable=self.month)
        self.month_Chosen['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,'2(闰年)')
        self.month_Chosen.grid(column=3, row=2)
        self.month_Chosen.current(0)

        self.T_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.T)
        self.T_entry.grid(column=3, row=3, sticky=(W, E))
        self.R_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.R)
        self.R_entry.grid(column=3, row=4, sticky=(W, E))
        self.P_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.P)
        self.P_entry.grid(column=3, row=5, sticky=(W, E))
        self.J_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.J)
        self.J_entry.grid(column=3, row=8, sticky=(W, E))
        self.H_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.H)
        self.H_entry.grid(column=3, row=6, sticky=(W, E))
        self.V_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.V)
        self.V_entry.grid(column=3, row=7, sticky=(W, E))


        #输出部分
        self.W0 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.W0).grid(column=6, row=3)
        self.W1 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.W1).grid(column=6, row=4)
        self.W2 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.W2).grid(column=6, row=5)
        self.W3 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.W3).grid(column=6, row=6)
        self.W4 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.W4).grid(column=6, row=7)
        self.P0 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.P0).grid(column=7, row=3)
        self.P1 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.P1).grid(column=7, row=4)
        self.P2 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.P2).grid(column=7, row=5)
        self.P3 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.P3).grid(column=7, row=6)
        self.P4 = StringVar()
        ttk.Label(self.mainframe, textvariable=self.P4).grid(column=7, row=7)

        self.point = IntVar()
        ttk.Label(self.mainframe, textvariable=self.point).grid(column=8, row=5)
        self.rank = StringVar()
        self.label2 = ttk.Label(self.mainframe, textvariable=self.rank)
        self.label2.grid(column=8, row=6)

        # self.showImg()
        
        #优化
        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.T_entry.focus()
        self.root.bind('<Return>', self.calculate)

    def showImg(self):
        load = Image.open(self.resImgSrc)
        img= ImageTk.PhotoImage(load) 
        label = ttk.Label(self.mainframe, image=render)
        # img.pack(side='top')
        # img.image = render 
        # img.place(x=10,y=10)


    def loadMap(self):

        reg = self.region_Chosen.get()
        res = (reg, self.rank.get())
        self.allResults.append(res)

        self.sf = shapefile.Reader(resource_path("./maps/zhuhai.shp"))
        shapes = self.sf.shapes()
        shapes_num = len(shapes)

        # plt
        if not self.firstDraw:
            plt.close(self.figNum)
            self.figNum += 1
            fig = plt.figure(self.figNum)
        else:
            self.firstDraw = False
            fig = plt.figure(self.figNum)
        ax = fig.add_subplot(111)
        ax.set_axis_bgcolor('grey')
        for nshp in range(shapes_num):
            ptchs = []
            pts = np.array(shapes[nshp].points)
            prt = shapes[nshp].parts
            par = list(prt) + [pts.shape[0]]

            for pij in range(len(prt)):
                ptchs = []
                vertices = []
                points = pts[par[pij]:par[pij+1]]

                poly = Polygon(points, facecolor='red')
                poly.set_facecolor('red')
                ptchs.append(poly)

                # ax.add_collection(PatchCollection(ptchs, facecolor=cccol[pij, :], linewidths=.5))
                ax.add_collection(PatchCollection(ptchs, facecolor=(1, 1, 1, 1), linewidths=.5))


        cm = get_cmap('Dark2')
        # print (len(prt))
        # cccol = cm(1.*np.arange(10)/len(prt))
        for res in self.allResults:
            pos = (self.regionMap[res[0]]['longitude'], self.regionMap[res[0]]['latitude'])
            level = self.levelMap[res[1]]
            cirl = Circle(xy=pos, facecolor=level, radius=0.015)
            ax.add_patch(cirl)

        # self.interpolate(ax)

        # print shapes[nshp].points
        x = [t[0] for t in shapes[nshp].points]
        y = [t[1] for t in shapes[nshp].points]
        xmax, xmin = max(x), min(x)
        ymax, ymin = max(y), min(y)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(21.7, 22.6)
        # ax.set_ylim(ymin, ymin + (xmax-xmin))

        fig.savefig('test.png')

        fig.show()

        print ('save!')

    def interpolate(self, ax):
        dx, dy = 0.03, 0.03
        for res in self.allResults:
            pos = (float(self.regionMap[res[0]]['longitude']), float(self.regionMap[res[0]]['latitude']))
            level = self.levelMap[res[1]]

            deltax, deltay, deltaz = 1-level[0], 1-level[1], 1-level[2]
            deltax, deltay, deltaz = deltax/7, deltay/7, deltaz/7

            pointRadius = 0.001
            curPos = (pos[0]-0.016, pos[1]-0.016)
            newColor = level
            for x in range(0, 7):
                newColor = (newColor[0]+deltax, newColor[1]+deltay, newColor[2]+deltaz, 1)
                print(newColor)
                for y in range(0, 10):
                    cirl = Circle(xy=curPos, facecolor=newColor, radius=pointRadius)
                    curPos = (curPos[0], curPos[1]+2*pointRadius)
                    ax.add_patch(cirl)

                for y in range(0, 10):
                    cirl = Circle(xy=curPos, facecolor=newColor, radius=pointRadius)
                    curPos = (curPos[0]+2*pointRadius, curPos[1])
                    ax.add_patch(cirl)

                for y in range(0, 10):
                    cirl = Circle(xy=curPos, facecolor=newColor, radius=pointRadius)
                    curPos = (curPos[0], curPos[1]-2*pointRadius)
                    ax.add_patch(cirl)

                for y in range(0, 10):
                    cirl = Circle(xy=curPos, facecolor=newColor, radius=pointRadius)
                    curPos = (curPos[0]-2*pointRadius, curPos[1])
                    ax.add_patch(cirl)

    #当月值/历史值按钮切换
    def switchBtn1Status(self):
        if self.J_entry.instate(['disabled']) :
            self.J_entry.state(['!disabled'])
            self.btn.config(text='使用当月值')
        else:
            self.J_entry.state(['disabled'])
            self.btn.config(text='使用历史值')

    def calculate(self, *args):
        #月均大气通风量使用当月实测计算值的情况
        if self.J_entry.instate(['!disabled']):
            #标准化
            if self.month_Chosen.get() == '2(闰年)':
                m = 13
            else:
                m = int(self.month.get())
            t = float(self.T.get())
            r = float(self.R.get())
            p = float(self.P.get())
            j = float(self.J.get())
            h = float(self.H.get())
            v = float(self.V.get())

            if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                rd = r/31
            elif m == 4 or m == 6 or m == 9 or m == 11:
                rd = r/30
            elif m == 13:
                rd = r/29
            else:
                rd = r/28

            if r<0 or p<0 or j<0 or h<0 or v<0:
                point.set('输入参数错误！')
            else:
                i = (1.8*t + 32) - 0.55*(1 - h/100)*(1.8*t - 26) - 3.2*v**0.5
                jr = 3.1536*0.001*3.1415926**0.5/2*j + 2.19*60*10*rd/(24*60*60)

                ta = [15.0,15.8,18.5,22.3,25.7,27.7,28.6,28.4,27.4,25.1,20.9,16.7,15.8]
                ra = [26.9,57.9,84.7,199.6,298.1,390.0,319.3,336.7,220.8,71.7,44.3,30.6,57.9]
                tt = (abs(t-ta[m-1])-10)/(0-10)*100
                rr = ((abs(r-ra[m-1]))**0.5-37.42)/(0-37.42)*100
                pp = (p-100)/(15-100)*100
                jj = (jr-5)/(20-5)*100
                ii = (abs(i-62.5)-22.5)/(0-22.5)*100

                #超出范围的数进行处理
                if tt>100:
                    tt = 100.0
                elif tt<0:
                    tt = 0.0
                if rr>100:
                    rr = 100.0
                elif rr<0:
                    rr = 0.0
                if pp>100:
                    pp = 100.0
                elif pp<0:
                    pp = 0.0
                if jj>100:
                    jj = 100.0
                elif jj<0:
                    jj = 0.0
                if ii>100:
                    ii = 100.0
                elif ii<0:
                    ii = 0.0

                #权重矩阵
                W = [[0.1391,0.1019,0.2673,0.2565,0.2353],
                     [0.1304,0.0940,0.2488,0.3044,0.2223],
                     [0.1355,0.0969,0.2576,0.2798,0.2302],
                     [0.1610,0.1031,0.2662,0.2233,0.2463],
                     [0.1458,0.1005,0.2668,0.2313,0.2556],
                     [0.1356,0.0973,0.2566,0.2172,0.2934],
                     [0.1511,0.1021,0.2692,0.2370,0.2405],
                     [0.1476,0.0981,0.2566,0.2501,0.2475],
                     [0.1330,0.0968,0.2548,0.2487,0.2668],
                     [0.1335,0.0968,0.2540,0.2341,0.2815],
                     [0.1540,0.0999,0.2634,0.2243,0.2584],
                     [0.1355,0.0990,0.2736,0.2606,0.2313],
                     [0.1304,0.0940,0.2488,0.3044,0.2223],]

                self.point.set(int(W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii))
                self.W0.set(W[m-1][0])
                self.W1.set(W[m-1][1])
                self.W2.set(W[m-1][2])
                self.W3.set(W[m-1][3])
                self.W4.set(W[m-1][4])
                self.P0.set(int(tt))
                self.P1.set(int(rr))
                self.P2.set(int(pp))
                self.P3.set(int(jj))
                self.P4.set(int(ii))
                if W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<21:
                    self.rank.set('恶劣')
                    self.label2.config(foreground='purple')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<41:
                    self.rank.set('差')
                    self.label2.config(foreground='red')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<56:
                    self.rank.set('中')
                    self.label2.config(foreground='#CC3300')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<70:
                    self.rank.set('良')
                    self.label2.config(foreground='#CC9900')
                else:
                    self.rank.set('优')
                    self.label2.config(foreground='green')
    #月均大气通风量使用程序内置历史值的情况
        elif self.J_entry.instate(['disabled']):
            #标准化
            JA = [4051.9,5578.6,4590.6,4069.7,5569.6,6197.8,6660.4,5281.1,5981.5,6336.2,4666.0,4994.8,5578.6]
            if self.month_Chosen.get() == '2(闰年)':
                m = 13
            else:
                m = int(month.get())
            t = float(self.T.get())
            r = float(self.R.get())
            p = float(self.P.get())
            j = JA[m-1]
            h = float(self.H.get())
            v = float(self.V.get())

            if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                rd = r/31
            elif m == 4 or m == 6 or m == 9 or m == 11:
                rd = r/30
            elif m == 13:
                rd = r/29
            else:
                rd = r/28

            if r<0 or p<0 or j<0 or h<0 or v<0:
                self.point.set('输入参数错误！')
            else:
                i = (1.8*t + 32) - 0.55*(1 - h/100)*(1.8*t - 26) - 3.2*v**0.5
                jr = 3.1536*0.001*3.1415926**0.5/2*j + 2.19*60*10*rd/(24*60*60)

                ta = [15.0,15.8,18.5,22.3,25.7,27.7,28.6,28.4,27.4,25.1,20.9,16.7,15.8]
                ra = [26.9,57.9,84.7,199.6,298.1,390.0,319.3,336.7,220.8,71.7,44.3,30.6,57.9]
                tt = (abs(t-ta[m-1])-10)/(0-10)*100
                rr = ((abs(r-ra[m-1]))**0.5-37.42)/(0-37.42)*100
                pp = (p-100)/(15-100)*100
                jj = (jr-5)/(20-5)*100
                ii = (abs(i-62.5)-22.5)/(0-22.5)*100

                #超出范围的数进行处理
                if tt>100:
                    tt = 100.0
                elif tt<0:
                    tt = 0.0
                if rr>100:
                    rr = 100.0
                elif rr<0:
                    rr = 0.0
                if pp>100:
                    pp = 100.0
                elif pp<0:
                    pp = 0.0
                if jj>100:
                    jj = 100.0
                elif jj<0:
                    jj = 0.0
                if ii>100:
                    ii = 100.0
                elif ii<0:
                    ii = 0.0

                #权重矩阵
                W = [[0.1391,0.1019,0.2673,0.2565,0.2353],
                     [0.1304,0.0940,0.2488,0.3044,0.2223],
                     [0.1355,0.0969,0.2576,0.2798,0.2302],
                     [0.1610,0.1031,0.2662,0.2233,0.2463],
                     [0.1458,0.1005,0.2668,0.2313,0.2556],
                     [0.1356,0.0973,0.2566,0.2172,0.2934],
                     [0.1511,0.1021,0.2692,0.2370,0.2405],
                     [0.1476,0.0981,0.2566,0.2501,0.2475],
                     [0.1330,0.0968,0.2548,0.2487,0.2668],
                     [0.1335,0.0968,0.2540,0.2341,0.2815],
                     [0.1540,0.0999,0.2634,0.2243,0.2584],
                     [0.1355,0.0990,0.2736,0.2606,0.2313],
                     [0.1304,0.0940,0.2488,0.3044,0.2223]]

                self.point.set(int(W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii))
                self.W0.set(W[m-1][0])
                self.W1.set(W[m-1][1])
                self.W2.set(W[m-1][2])
                self.W3.set(W[m-1][3])
                self.W4.set(W[m-1][4])
                self.P0.set(int(tt))
                self.P1.set(int(rr))
                self.P2.set(int(pp))
                self.P3.set(int(jj))
                self.P4.set(int(ii))
                if W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<21:
                    self.rank.set('恶劣')
                    self.label2.config(foreground='purple')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<41:
                    self.rank.set('差')
                    self.label2.config(foreground='red')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<56:
                    self.rank.set('中')
                    self.label2.config(foreground='#CC3300')
                elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<70:
                    self.rank.set('良')
                    self.label2.config(foreground='#CC9900')
                else:
                    self.rank.set('优')
                    self.label2.config(foreground='green')

        self.loadMap()
    



def main():
    root = Tk()
    app = EvaluationSystem(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()



