from tkinter import *
from tkinter import *
from PIL import Image, ImageTk
from math import *
class Window:
    def __init__(self, size, w=None, h=None, fill=None):
        self._win  = Tk()
        self._win.title("allo game window")
        self._winsize = self._win.geometry(size)
        self._resize = self._win.resizable(width=False, height=False)
        self._c = Canvas(self._win, width=w, height=h, bg=fill)
        self._c.pack()

    def title(self,title):
        self._win.title(title)

    def update(self):
        self._win.update()
        
    def icon(self,path):
        self.icon = window.iconbitmap(path)        
            
    def delete(self, object):
        self._c.delete(object)

###################################
#             DRAW
###################################

    def load_image(self,x,y,image,anchor):
        self.img = Image.open(image)
        self.self._c.image = ImageTk.PhotoImage(self.img)
        self._c.create_image(x,y,image=self.c.image,anchor=anchor)

    def create_text(self,x,y,color=None,text=''):
        self._c.create_text(x,y,fill=color,text=text)
    def draw_polygon(self,p1,p2,p3,p4,p5,p6,fill=None,outline=None):
        self._c.create_polygon(p1,p2,p3,p4,p5,p6,fill=fill,outline=outline)

    def draw_rectangle(self,p1,p2,p3,p4,fill=None,outline=None):
        self._c.create_rectangle(p1,p2,p3,p4,fill=fill,outline=outline)

    def draw_oval(self,p1,p2,p3,p4,fill=None,outline=None):
        self._c.create_oval(p1,p2,p3,p4,fill=fill,outline=outline)

    def draw_line(self,p1,p2,p3,p4):
        self._c.create_line(p1,p2,p3,p4)
        
    def main_loop(self):
        self._win.mainloop()
