"""
A simple input window with an entry, a few buttons, and a popup window to display the input.
"""

from ttkbootstrap import Style
from tkinter import ttk
import tkinter
from tkinter.messagebox import showinfo

style = Style() # default style is lumen
window = style.master
window.title('Window Title')

user_input = tkinter.StringVar()
ttk.Label(window, text="A simple window demonstration").pack(side='top', fill='x', padx=10, pady=10)
ttk.Entry(window, textvariable=user_input, width=50).pack(side='top', fill='x', padx=10, pady=10)
ttk.Button(window, text="Submit", command=lambda: showinfo(message=user_input.get())).pack(side='left', padx=10, pady=10)
ttk.Button(window, text="Cancel", command=window.quit).pack(side='left', padx=10, pady=10)

window.mainloop()

