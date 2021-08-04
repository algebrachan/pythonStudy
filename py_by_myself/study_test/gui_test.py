import tkinter

if __name__ == '__main__':
    top = tkinter.Tk(screenName='wc')
    # label = tkinter.Label(top,text='hello world!')
    # label.pack()
    quit = tkinter.Button(top,text='hello world!',command=top.quit())
    quit.pack()
    tkinter.mainloop()