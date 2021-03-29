#coding:utf-8
from sys import version
import os,time,requests,json,threading

__all__=["file_operations","time_class","network","text","thread"]

class a():
    def __init__(self):
        pass
    def file_exists(self,path):
        if not os.path.exists(path):
            return True
        else:
            return False

    def file_remove(self,path):
        os.remove(path)

    def create_folder(self,path):
        os.mkdir(path)

    def path_get_file_name(self,path):
        return path.split('\\')[-1]

    def file_name_get_suffix_name(self,fill_name):
        return fill_name.split('.')[-1]
class b():
    def __init__(self):
        pass
    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')
    def time_sleep(self,stime):
        time.sleep(stime)

class c():
    def __init__(self):
        pass
    def get_url(self,url):
        return requests.get(url=url)

    def file_downloads(self,url, path):
        r = requests.get(url, stream=True)
        f = open(path, 'wb')
        for a in r.iter_content(chunk_size=100):  # iter是iter
            f.write(a)

class d():
    def __init__(self):
        pass
    def parsing_text(self,text):
        return json.load(text)

class e():
    def __init__(self):
        pass

    def start(self,methods, parameter):
        m = threading.Thread(target=methods, args=parameter)
        m.start()

file_operations = a()
time_class = b()
network = c()
text = d()
thread = e()


print("Multifunction 0.0.3 (Python",version,")")