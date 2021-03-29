import os, time
import requests

class gui:
    cur = ''
    nl = '<br />'
    def title(self, title):
        self.cur = f'<title>{title}</title>'
    def ext(self, text):
        self.cur += f'<p>{text}</p>'
    def newline(self):
        self.cur += '<br />'
    def button(self, displayname, ref):
        self.cur += f'<button id="{ref}">{displayname}</button>'
    def to_html(self):
        from bs4 import BeautifulSoup as b
        hta = b(self.cur, 'html.parser')
        print(hta.prettify())
    def button_onclick_js(self, displayname, js):
        self.cur += f'<button onclick="{js}">{displayname}</button>'
    def text_input(self, displayname, ref):
        self.cur += f'<input placeholder="{displayname}" id="{ref}"' + '></input>'
    def js(self, js):
        self.cur += f'<script>{js}</script>'
    def start_as_app(self):
        open('gui.hta','w').write(self.cur)
        os.system('start gui.hta')
    def start_as_site(self):
        open('gui.html','w').write(self.cur)
        os.system('start gui.html')
    def start_as_chrome_app(self):
        open('gui.html','w').write(self.cur)
        os.system('start chrome --app="%cd%\gui.html"')
    def reset_gui(self):
        self.cur = ''
    def mimic_site(self, site):
        self.cur = requests.get(site).content.decode()
    def stop(self, ext):
        os.system(f'del gui.{ext}')
        
    
    
        

        
