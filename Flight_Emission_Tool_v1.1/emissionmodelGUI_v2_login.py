from tkinter import *
from lib.emissionmodelGUI_v2 import*

import lib

class Authentication:
    user = 'admin'
    passw = 'admin'

    def __init__(self, root):
        self.root = root
        self.root.title('USER AUTHENTICATION')

        rows = 0
        while rows < 10:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows += 1


        frame = LabelFrame(self.root, text='Login')
        frame.grid(row=1, column=1, columnspan=10, rowspan=10)

        Label(frame, text=' Usename ').grid(row=2, column=1, sticky=W)
        self.username = Entry(frame)
        self.username.grid(row=2, column=2)

        Label(frame, text=' Password ').grid(row=5, column=1, sticky=W)
        self.password = Entry(frame, show='*')
        self.password.grid(row=5, column=2)

        ttk.Button(frame, text='LOGIN', command=self.login_user).grid(row=7, column=2)

        self.message = Label(text='', fg='Red')
        self.message.grid(row=9, column=6)

    def login_user(self):
        if self.username.get() == self.user and self.password.get() == self.passw:
            root.destroy()

            newroot = emissionmodelGUI_App()
            newroot.mainloop()

        else:
            self.message['text'] = 'Username or Password incorrect. Try again!'


if __name__ == '__main__':
    root = Tk()
    root.geometry('425x185+700+300')
    application = Authentication(root)
    root.mainloop()