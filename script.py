import sys
from genericpath import exists
import requests
import json
from collections import namedtuple
import shutil
import os

base_url = "https://nekos.life/api/v2/img/"

file = open("categories", "r")
categories = file.readlines()


if not os.path.exists("img"):
    os.mkdir("img")
os.chdir("img")

for c in categories:
    c = c.strip("\n")
    if not os.path.exists(c):
        os.mkdir(c)
    f = 0
    os.chdir(c)
    i = len([name for name in os.listdir('.') if os.path.isfile(name)])


    while f <= i + 5:
        filename = ""
        with requests.Session() as s:
            api_output = s.get(base_url + c)

        output = api_output.text

        x = json.loads(output, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        url = x.url
        filename = url[url.rfind("/")+1:]
        exists = os.path.exists(filename)

        
        sys.stdout.write('\x1b[1A') 
        sys.stdout.write('\x1b[2K') 

        if not exists:
            grab = requests.get(url, stream=True)
            if grab.status_code == 200:
                with open(filename, "wb") as f:
                    grab.raw.decode_content = True
                    shutil.copyfileobj(grab.raw, f)
            print("Sucessfully downloaded " + filename)
            f = 0
            i = len([name for name in os.listdir('.') if os.path.isfile(name)])
        else:
            f += 1
        print("Category: " + c + " (" + str(categories.index(c + "\n") + 1) + "/" + str(categories.__len__()) + ") Img: " + str(i) + " Failed: " + str(f))

    os.chdir("..")
