import tkinter as tk
import random
import tkinter.font as tf
import threading

hex_massage = ''
temp_massage = ''
code = 0


def get_OriMassage():
    massage = box_Input.get('1.0', 'end-1c')
    massage_by = bytes(massage, 'UTF-8')  # 先将输入的字符串转化成字节码
    global hex_massage
    hex_massage = massage_by.hex()

    clean_box()

    box_FinOut.insert('insert', hex_massage)
    if len(hex_massage) > 128:
        box_OriginLen.insert('insert', "512*%d+%d=" % ((4 * len(hex_massage)) // 512, (4 * len(hex_massage)) % 512))
    box_OriginLen.insert('insert', "%dbits(%s)" % (4 * len(hex_massage), hex(4 * len(hex_massage))))

    if var_format.get() == 1:
        format_solve()


def get_massage():  # 获取明文串
    get_OriMassage()
    global code
    code = 1


def do_nothing(event):  # 屏蔽回车
    return 'break'


def random_input():
    num = random.randint(1, 96)

    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    clean_all()
    box_Input.insert('end', salt)


def clean_box():
    box_FinOut.delete('1.0', 'end')
    box_OriginLen.delete('1.0', 'end')
    box_FinalLen.delete('1.0', 'end')
    global code
    code = 0


def clean_all():
    box_Input.delete('1.0', 'end')
    clean_box()


def get_Expand():
    n = 0
    global hex_massage
    global temp_massage
    get_OriMassage()
    proc_massage = hex_massage
    temp_massage = box_FinOut.get('1.0', 'end-1c')
    box_FinOut.delete('1.0', 'end')
    box_FinalLen.delete('1.0', 'end')
    format_dim = hex(4 * len(proc_massage))[2:]  # 末尾增加的长度并格式化

    proc_massage = proc_massage + '8'
    # while  > 512,print hex_massage[512]
    #   hex_massage = hex_massage[512:] (先处理前面的任意长度组, 剩下长度<512)，
    while len(proc_massage) > 128:
        hex_massage_b1 = proc_massage[0:128]
        box_FinOut.insert('end', hex_massage_b1)
        proc_massage = proc_massage[128:]
        n = n + 1

    # 大于448时
    if len(proc_massage) > 112:
        #   大于448是要填充第二组，可以直接设置长度1024修改
        while len(proc_massage) != 256 - len(str(format_dim)):
            proc_massage = proc_massage + '0'
    # 小于448时的填充
    if len(proc_massage) <= 112:
        while len(proc_massage) != 128 - len(str(format_dim)):
            proc_massage = proc_massage + '0'
    proc_massage = proc_massage + str(format_dim)
    box_FinOut.insert('end', proc_massage)
    box_FinalLen.insert('end', "%dbits(%s)" % (4 * len(proc_massage) + n * 512, hex(4 * len(proc_massage) + n * 512)))

    if var_format.get() == 1:
        format_solve()


def expand_code():
    get_Expand()
    global code
    code = 2


def get_Color():
    if var_format == 1:
        str_1 = hex_massage
    else:
        str_1 = temp_massage
    str_2 = box_FinOut.get('1.0', 'end-1c')  # 填充后消息
    box_FinOut.tag_add('tag1', '1.0', '1.%d' % len(str_1))
    if var_format.get() == 1:
        box_FinOut.tag_add('tag2', '1.%d' % len(str_1), '1.%d' % (len(str_2) - 9))
        box_FinOut.tag_add('tag3', '1.%d' % (len(str_2) - 9), '1.end')
    else:
        box_FinOut.tag_add('tag2', '1.%d' % len(str_1), '1.%d' % (len(str_2) - 8))
        box_FinOut.tag_add('tag3', '1.%d' % (len(str_2) - 8), '1.end')

    box_FinOut.tag_config('tag1', foreground='MediumSeaGreen')
    box_FinOut.tag_config('tag2', foreground='red')
    box_FinOut.tag_config('tag3', foreground='RoyalBlue')


def color_solve():
    get_Color()
    global code
    code = 3


def format_solve():
    str_2 = box_FinOut.get('1.0', 'end-1c')
    for i in range(len(str_2) + len(str_2) // 8):
        while (i + 1) % 9 == 0:
            box_FinOut.insert('1.%d' % i, '\t')
            i = i + 1


def get_format():
    if code == 1:
        get_massage()
    elif code == 2:
        get_massage()
        expand_code()
    elif code == 3:
        get_massage()
        expand_code()
        color_solve()

    if var_format.get() == 1:
        w1.delete(tk.ALL)
        w1.create_line(3, 0, 3, 25)  # 纵
        w1.create_line(93, 0, 93, 25)

        w1.create_line(104, 0, 104, 25)
        w1.create_line(194, 0, 194, 25)

        w1.create_line(205, 0, 205, 25)
        w1.create_line(295, 0, 295, 25)

        w1.create_line(306, 0, 306, 25)
        w1.create_line(396, 0, 396, 25)

        w1.create_line(3, 14, 93, 14)  # 横
        w1.create_line(104, 14, 194, 14)
        w1.create_line(205, 14, 295, 14)
        w1.create_line(306, 14, 396, 14)
        w1.create_text(51, 8, text="8 bits", font=("Courier", 10))
        w1.create_text(149, 8, text="8 bits", font=("Courier", 10))
        w1.create_text(250, 8, text="8 bits", font=("Courier", 10))
        w1.create_text(351, 8, text="8 bits", font=("Courier", 10))
    else:
        w1.delete(tk.ALL)
        w1.create_line(3, 0, 3, 25)
        w1.create_line(410, 0, 410, 25)
        w1.create_line(3, 14, 410, 14)
        w1.create_text(203, 8, text="36 bits", font=("Courier", 10))
        w1.create_text(9, 19, text="01", font=("Courier", 9))
        w1.create_text(19, 19, text="02", font=("Courier", 9))
        w1.create_text(30, 19, text="03", font=("Courier", 9))
        w1.create_text(41, 19, text="04", font=("Courier", 9))
        w1.create_text(53, 19, text="05", font=("Courier", 9))
        w1.create_text(64, 19, text="06", font=("Courier", 9))
        w1.create_text(75, 19, text="07", font=("Courier", 9))
        w1.create_text(86, 19, text="08", font=("Courier", 9))

        w1.create_text(98, 19, text="09", font=("Courier", 9))
        w1.create_text(109, 19, text="10", font=("Courier", 9))
        w1.create_text(120, 19, text="11", font=("Courier", 9))
        w1.create_text(131, 19, text="12", font=("Courier", 9))
        w1.create_text(142, 19, text="13", font=("Courier", 9))
        w1.create_text(153, 19, text="14", font=("Courier", 9))
        w1.create_text(164, 19, text="15", font=("Courier", 9))
        w1.create_text(175, 19, text="16", font=("Courier", 9))

        w1.create_text(187, 19, text="17", font=("Courier", 9))
        w1.create_text(198, 19, text="18", font=("Courier", 9))
        w1.create_text(209, 19, text="19", font=("Courier", 9))
        w1.create_text(221, 19, text="20", font=("Courier", 9))
        w1.create_text(232, 19, text="21", font=("Courier", 9))
        w1.create_text(243, 19, text="22", font=("Courier", 9))
        w1.create_text(254, 19, text="23", font=("Courier", 9))
        w1.create_text(265, 19, text="24", font=("Courier", 9))

        w1.create_text(276, 19, text="25", font=("Courier", 9))
        w1.create_text(287, 19, text="26", font=("Courier", 9))
        w1.create_text(298, 19, text="27", font=("Courier", 9))
        w1.create_text(310, 19, text="28", font=("Courier", 9))
        w1.create_text(321, 19, text="29", font=("Courier", 9))
        w1.create_text(332, 19, text="30", font=("Courier", 9))
        w1.create_text(344, 19, text="31", font=("Courier", 9))
        w1.create_text(355, 19, text="32", font=("Courier", 9))

        w1.create_text(366, 19, text="33", font=("Courier", 9))
        w1.create_text(377, 19, text="34", font=("Courier", 9))
        w1.create_text(389, 19, text="35", font=("Courier", 9))
        w1.create_text(400, 19, text="36", font=("Courier", 9))


def auto_fill():
    if var_AutoPut.get() == 1:
        bot_process.configure(state='disabled')
    else:
        bot_process.configure(state='normal')

    if var_AutoExp.get() == 1:
        bot_fill.configure(state='disabled')
        var_AutoPut.set(1)
    else:
        bot_fill.configure(state='normal')

    if var_AutoColor.get() == 1:
        bot_color.configure(state='disabled')

        var_AutoPut.set(1)
        var_AutoExp.set(1)
    else:
        bot_color.configure(state='normal')

    if var_AutoPut.get() == 1 and code <= 1:
        get_OriMassage()
        bot_color.configure(state='disabled')

    if var_AutoExp.get() == 1 and code <= 2:
        get_Expand()
        bot_color.configure(state='normal')

    if var_AutoColor.get() == 1 and code <= 3:
        get_Color()
        bot_color.configure(state='disabled')

    global timer
    timer = threading.Timer(0.5, auto_fill)
    timer.start()


# GUI区域
root = tk.Tk()
root.title(u"SHA-256填充")

var_format = tk.IntVar()
check_format = tk.Checkbutton(root, text='格式输出', variable=var_format, onvalue=1, offvalue=0, command=get_format)
var_format.set(1)

var_AutoPut = tk.IntVar()
check_AutoPut = tk.Checkbutton(root, text='自动处理', variable=var_AutoPut, onvalue=1, offvalue=0)

var_AutoExp = tk.IntVar()
check_AutoExp = tk.Checkbutton(root, text='自动填充', variable=var_AutoExp, onvalue=1, offvalue=0)

var_AutoColor = tk.IntVar()
check_AutoColor = tk.Checkbutton(root, text='自动填色', variable=var_AutoColor, onvalue=1, offvalue=0)

w = tk.Canvas(root, width=640, height=150)  # 图
w.grid(row=0, column=0, columnspan=4, rowspan=3)

w.create_rectangle(20, 40, 330, 80, fill="MediumSeaGreen")
w.create_text(70, 60, text="Massage", font=("Courier", 12))
w.create_rectangle(330, 40, 500, 80, fill="LightCoral")
w.create_text(380, 60, text="Padding", font=("Courier", 12))
w.create_rectangle(500, 40, 630, 80, fill="RoyalBlue")
w.create_text(550, 60, text="Length", font=("Courier", 12))

w.create_line(20, 80, 20, 100)  # 纵
w.create_line(630, 80, 630, 100)
w.create_line(20, 90, 160, 90)  # 横
w.create_line(380, 90, 630, 90)
w.create_text(270, 90, text="Length = Multiple of 512 bits", font=("Courier", 12))

w.create_line(500, 20, 500, 40)  # 纵
w.create_line(630, 20, 630, 40)
w.create_line(500, 30, 540, 30)  # 横
w.create_line(590, 30, 630, 30)
w.create_text(565, 30, text="64 bits", font=("Courier", 10))

w1 = tk.Canvas(root, width=408, height=20)  # 标
w1.grid(row=2, column=2, columnspan=2, rowspan=1, sticky='s')

w2 = tk.Canvas(root, width=224, height=20)  # 标
w2.grid(row=4, column=0, columnspan=2, rowspan=1, sticky='n')

w2.create_line(0, 13, 226, 13)
w2.create_line(3, 0, 3, 25)  # 纵
w2.create_line(226, 0, 226, 25)
w2.create_text(100, 7, text="32 bits", font=("Courier", 10))
get_format()

label_1 = tk.Label(root, text="⬇输入原始报文")
label_1.grid(row=2, column=0, sticky='s')
label_2 = tk.Label(root, text="️原报文长度")
label_2.grid(row=0, column=0, sticky='wn')

# ft0 = tf.Font(family='LCD BQ', size=16)
# ft1 = tf.Font(family='Spot Mono', size=16)
ft0 = tf.Font(family='Pixel LCD7', size=16)
ft1 = tf.Font(family='Courier', size=12)

box_Input = tk.Text(root, height='12', width='32')  # 输入框
box_FinOut = tk.Text(root, height='18', width='34', font=ft0)  # 扩后

box_OriginLen = tk.Text(root, height='1', width='28', font=ft1)  # ori长度
box_OriginLen.grid(row=0, column=0, sticky='e', columnspan=2)
box_FinalLen = tk.Text(root, height='1', width='16', font=ft1)  # fin长度
box_FinalLen.grid(row=2, column=2, sticky='n', columnspan=2)

box_Input.bind('<Return>', do_nothing)

bot_random = tk.Button(root, text="随机报文", command=random_input)
bot_process = tk.Button(root, text="处理", command=get_massage)
bot_fill = tk.Button(root, text="填充", command=expand_code)
bot_clean = tk.Button(root, text="清除", command=clean_all)
bot_color = tk.Button(root, text="填色", command=color_solve)

box_Input.grid(row=3, column=0, columnspan=2, sticky='w')

box_FinOut.grid(row=3, column=2, rowspan=6, columnspan=2, sticky='s')

bot_random.grid(row=2, column=1, sticky='s')
bot_clean.grid(row=5, column=0)
bot_process.grid(row=6, column=0)
bot_fill.grid(row=7, column=0)
bot_color.grid(row=8, column=0)

check_format.grid(row=5, column=1, sticky='w')
check_AutoPut.grid(row=6, column=1, sticky='w')
check_AutoExp.grid(row=7, column=1, sticky='w')
check_AutoColor.grid(row=8, column=1, sticky='w')

auto_fill()

root.mainloop()
