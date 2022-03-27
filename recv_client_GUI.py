# coding=utf-8

from Tkinter import *
import ttk

from zeroconf import Zeroconf
from socket import *
 
import time
from threading import Timer

connect_target = ()

class Listener:
 
    def add_service(self, zeroconf, serviceType, name):
 
        info = zeroconf.get_service_info(serviceType, name)

        global connect_target
        connect_target = (str(inet_ntoa(info.address)), int(info.port))
 
zconf = Zeroconf()
 
serviceListener = Listener()
 
zconf.add_service_listener("_fdx-b._tcp.local.", serviceListener)

s = socket(AF_INET,SOCK_STREAM)


def show_load_page():
    global BP
    BP = Frame(root)
    BP.pack()
    Pb = ttk.Progressbar(BP, length=400, mode="indeterminate",orient=HORIZONTAL)
    Pl = Label(BP, text="连接设备中....", font=("simhei", 20))
    Pl.pack()
    Pb.pack()
    Pb.start(1)

def show_work_page():
    # for widget in root.winfo_children():
    #     widget.destroy()

    tabel_frame = Frame(root)
    tabel_frame.pack()

    yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

    columns = ['序号', '时间', '芯片码']
    global table
    table = ttk.Treeview(
            master=tabel_frame,  # 父容器
            height=10,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列

            yscrollcommand=yscroll.set,  # y轴滚动条
            )

    for column in columns:
        table.heading(column=column, text=column, anchor=CENTER)  # 定义表头
        table.column(column=column, width=100, minwidth=100, anchor=CENTER, )  # 定义列

    yscroll.config(command=table.yview)
    yscroll.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=True)

    btn_frame = Frame()
    btn_frame.pack()
    Button(btn_frame, text='导出CSV', bg='yellow', width=20, command=export_csv).pack(side=LEFT)
    Button(btn_frame, text='清空', bg='yellow', width=20, command=table_clear).pack(side=LEFT)


def export_csv():
    pass

def table_clear():
    pass


def Timer1_create():
    global t1
    t1 = Timer(5, ready_check, ())
    t1.start()

def ready_check():
    print connect_target
    if connect_target:
        s.connect(connect_target)
        s.setblocking(False)
        zconf.close()

        # show_work_page()
        Timer2_create()
    else:
        Timer1_create()

def Timer2_create():
    global t2
    t2 = Timer(2, recv_listener, ())
    t2.start()

def recv_listener():
    print '.'
    try:
        data = s.recv(1024)
        print data
        lastNo = len(table.get_children())
        print lastNo
        display_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print display_time
        table.insert('', END, values=[lastNo+1, display_time, data])  # 添加数据到末尾
    except error:
        pass
    Timer2_create()


def closeWindow():
    try:
        t1.cancel()
        t2.cancel()
        zconf.close()
        s.close()
    except NameError:
        pass
    root.destroy()

if __name__ == '__main__':
    root = Tk()  # 窗口
    root.title("FDX-B Host Terminal")  # 标题
    screenwidth = root.winfo_screenwidth()  # 屏幕宽度
    screenheight = root.winfo_screenheight()  # 屏幕高度
    width = 500
    height = 300
    x = int((screenwidth - width) / 2)
    y = int((screenheight - height) / 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

    # show_load_page()
    show_work_page()

    Timer1_create()

    root.protocol('WM_DELETE_WINDOW', closeWindow)
    root.mainloop()