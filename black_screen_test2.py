import tkinter
import sys

# 第4种方法，无需使用线程，用户在界面上输入study后退出。（目前推荐使用）
root = tkinter.Tk()
root.overrideredirect(True)
root.config(bg="Black")
x,y = root.winfo_screenwidth(),root.winfo_screenheight()  # 等于屏幕分辨率（像素）
x, y = str(x), str(y) # x = str((x-1000)) 替换为本行及下面行以让黑窗口左侧有1000空隙
root.geometry((x+"x"+y+'+0+0'))  # root.geometry((x+"x"+y+'+1000+0')) 替换为本行及上面行以让黑窗口左侧有1000空隙
root.wm_attributes("-topmost", 1)  # 一定要最后测试号再设置为置顶，否则无法操作，只能重启系统！！！


########## 第4种方法 begin ###########
def get_value():
    input_str =  entry.get()
    if input_str == 'study':
        root.quit()
        sys.exit()


entry = tkinter.Entry(root)
entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
button = tkinter.Button(root, text='请在上面输入框里输入"study"以退出黑屏', command=get_value)
button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
########## 第4种方法 end ###########

root.mainloop()
