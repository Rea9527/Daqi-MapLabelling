from tkinter import *
from tkinter import ttk

root = Tk()
root.title("气象宜居指数计算系统")
mainframe = ttk.Frame(root, padding="6 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#定义函数

#当月值/历史值按钮切换
def switchBtn1Status():
    if J_entry.instate(['disabled']) :
        J_entry.state(['!disabled'])
        btn.config(text='使用当月值')
    else:
        J_entry.state(['disabled'])
        btn.config(text='使用历史值')


def calculate(*args):
#月均大气通风量使用当月实测计算值的情况
    if J_entry.instate(['!disabled']):
        #标准化
        if month_Chosen.get() == '2(闰年)':
            m = 13
        else:
            m = int(month.get())
        t = float(T.get())
        r = float(R.get())
        p = float(P.get())
        j = float(J.get())
        h = float(H.get())
        v = float(V.get())

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

            point.set(int(W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii))
            W0.set(W[m-1][0])
            W1.set(W[m-1][1])
            W2.set(W[m-1][2])
            W3.set(W[m-1][3])
            W4.set(W[m-1][4])
            P0.set(int(tt))
            P1.set(int(rr))
            P2.set(int(pp))
            P3.set(int(jj))
            P4.set(int(ii))
            if W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<21:
                rank.set('恶劣')
                label2.config(foreground='purple')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<41:
                rank.set('差')
                label2.config(foreground='red')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<56:
                rank.set('中')
                label2.config(foreground='#CC3300')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<70:
                rank.set('良')
                label2.config(foreground='#CC9900')
            else:
                rank.set('优')
                label2.config(foreground='green')
#月均大气通风量使用程序内置历史值的情况
    elif J_entry.instate(['disabled']):
        #标准化
        JA = [4051.9,5578.6,4590.6,4069.7,5569.6,6197.8,6660.4,5281.1,5981.5,6336.2,4666.0,4994.8,5578.6]
        if month_Chosen.get() == '2(闰年)':
            m = 13
        else:
            m = int(month.get())
        t = float(T.get())
        r = float(R.get())
        p = float(P.get())
        j = JA[m-1]
        h = float(H.get())
        v = float(V.get())

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
                 [0.1304,0.0940,0.2488,0.3044,0.2223]]

            point.set(int(W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii))
            W0.set(W[m-1][0])
            W1.set(W[m-1][1])
            W2.set(W[m-1][2])
            W3.set(W[m-1][3])
            W4.set(W[m-1][4])
            P0.set(int(tt))
            P1.set(int(rr))
            P2.set(int(pp))
            P3.set(int(jj))
            P4.set(int(ii))
            if W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<21:
                rank.set('恶劣')
                label2.config(foreground='purple')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<41:
                rank.set('差')
                label2.config(foreground='red')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<56:
                rank.set('中')
                label2.config(foreground='#CC3300')
            elif W[m-1][0]*tt + W[m-1][1]*rr + W[m-1][2]*pp + W[m-1][3]*jj + W[m-1][4]*ii<70:
                rank.set('良')
                label2.config(foreground='#CC9900')
            else:
                rank.set('优')
                label2.config(foreground='green')
        pass

#文本与按钮部分
ttk.Label(mainframe, text="月份").grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, text="月均气温(℃)").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="月降水量(mm)").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="月均AQI").grid(column=2, row=5, sticky=W)
ttk.Label(mainframe, text="月均大气通风量(m2/s)").grid(column=2, row=8, sticky=W)
ttk.Label(mainframe, text="月均湿度(%)").grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text="月均地面风速(m/s)").grid(column=2, row=7, sticky=W)
ttk.Label(mainframe, text="                 ").grid(column=4, row=3, sticky=W)
ttk.Label(mainframe, text="指标").grid(column=5, row=2)
ttk.Label(mainframe, text="气温").grid(column=5, row=3)
ttk.Label(mainframe, text="降水量").grid(column=5, row=4)
ttk.Label(mainframe, text="污染物浓度").grid(column=5, row=5)
ttk.Label(mainframe, text="大气净化能力").grid(column=5, row=6)
ttk.Label(mainframe, text="人体舒适度").grid(column=5, row=7)
ttk.Label(mainframe, text="各项权重  ").grid(column=6, row=2)
ttk.Label(mainframe, text="各项得分  ").grid(column=7, row=2)
ttk.Label(mainframe, text="气象宜居指数得分").grid(column=8, row=7, sticky=W)
ttk.Button(mainframe, text="计算", command=calculate).grid(column=3, row=9, sticky=W)

btn = ttk.Button(mainframe, text='使用当月值', command=switchBtn1Status)
btn.grid(column=4, row=8, sticky=W)

#输入部分
month = StringVar()
T = StringVar()
R = StringVar()
P = StringVar()
J = StringVar()
H = StringVar()
V = StringVar()

month_Chosen = ttk.Combobox(mainframe, width=9, textvariable=month)
month_Chosen['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,'2(闰年)')
month_Chosen.grid(column=3, row=2)
month_Chosen.current(0)

T_entry = ttk.Entry(mainframe, width=7, textvariable=T)
T_entry.grid(column=3, row=3, sticky=(W, E))
R_entry = ttk.Entry(mainframe, width=7, textvariable=R)
R_entry.grid(column=3, row=4, sticky=(W, E))
P_entry = ttk.Entry(mainframe, width=7, textvariable=P)
P_entry.grid(column=3, row=5, sticky=(W, E))
J_entry = ttk.Entry(mainframe, width=7, textvariable=J)
J_entry.grid(column=3, row=8, sticky=(W, E))
H_entry = ttk.Entry(mainframe, width=7, textvariable=H)
H_entry.grid(column=3, row=6, sticky=(W, E))
V_entry = ttk.Entry(mainframe, width=7, textvariable=V)
V_entry.grid(column=3, row=7, sticky=(W, E))


#输出部分
W0 = StringVar()
ttk.Label(mainframe, textvariable=W0).grid(column=6, row=3)
W1 = StringVar()
ttk.Label(mainframe, textvariable=W1).grid(column=6, row=4)
W2 = StringVar()
ttk.Label(mainframe, textvariable=W2).grid(column=6, row=5)
W3 = StringVar()
ttk.Label(mainframe, textvariable=W3).grid(column=6, row=6)
W4 = StringVar()
ttk.Label(mainframe, textvariable=W4).grid(column=6, row=7)
P0 = StringVar()
ttk.Label(mainframe, textvariable=P0).grid(column=7, row=3)
P1 = StringVar()
ttk.Label(mainframe, textvariable=P1).grid(column=7, row=4)
P2 = StringVar()
ttk.Label(mainframe, textvariable=P2).grid(column=7, row=5)
P3 = StringVar()
ttk.Label(mainframe, textvariable=P3).grid(column=7, row=6)
P4 = StringVar()
ttk.Label(mainframe, textvariable=P4).grid(column=7, row=7)

point = IntVar()
ttk.Label(mainframe, textvariable=point).grid(column=8, row=5)
rank = StringVar()
label2 = ttk.Label(mainframe, textvariable=rank)
label2.grid(column=8, row=6)


#优化
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
T_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
