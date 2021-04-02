'''
  A minimalist Notepad built with TKinter framework
  Author:     Israel Dryer
  Email:      israel.dryer@gmail.com
  Modified:   2020-06-19
'''
from ttkbootstrap import Style
from tkinter import ttk
import tkinter


style = Style(theme='journal')
window = style.master
print(style.themes)

frame = ttk.Frame(window, padding=15)
frame.pack(fill='both', expand='yes')

info_frame = ttk.Frame(frame, style='success.TFrame')
info_frame.pack(fill='x')
info_var = tkinter.StringVar(value='<new file>')

# customize label background for infobar
style.configure('infobar.TLabel', background=style.colors.success, foreground=style.colors.selectfg)
ttk.Label(info_frame, textvariable=info_var, style='infobar.TLabel').pack(padx=10, pady=10)


window.mainloop()