#Imports
import urllib.request
import re

#Watch Function
def watch(name : str):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + name)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    link = "https://www.youtube.com/watch?v=" + video_ids[0]
    return link