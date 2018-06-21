# -*- coding utf-8 -*-
__author__ = 'Maybe'

import requests

# from tkinter import *
#
# root = Tk()
# root.title("品类")
# root.geometry('300x300')
#
#
# l1 = Label(root, text="品类名：")
# l1.pack()
# type_text = StringVar()
# type = Entry(root, textvariable = type_text)
# type_text.set(" ")
# type.pack()
#
#
# def on_click():
#     x = type_text.get()
#     string = str("type名：%s " % (x))
#     print("type名：%s " % (x))
#     # messagebox.showinfo(title='aaa', message=string)
#
#
# Button(root, text="press", command=on_click).pack()
# root.mainloop()

IP = {
    'http':'http://115.223.204.123:9000',
}
a = requests.get('https://detail.tmall.com/item.htm?id=45791147497&ns=1&abbucket=12', proxies=IP)
print (a.text)