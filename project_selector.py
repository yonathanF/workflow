#!/usr/bin/env python3
from rofi import Rofi
import subprocess
from os import path

topics = ["Simple Chisel", "Scala Learning", "Simple Tex", "Temp Course"]
paths = ["/home/yonathan/Projects/Research/SimpleChisel/",
         "/home/yonathan/Projects/SideProjects/scala/",
         "/home/yonathan/Projects/SideProjects/SimpleTex/",
         "/home/yonathan/Courses/Temp-Course/"]
r = Rofi(rofi_args=["-i"])
index, key = r.select("Choose a project: ", topics)

if index != -1:
    subprocess.Popen(["unlink", "/home/yonathan/active-topic"])
    subprocess.Popen(["ln", "-s", paths[index],
                      "/home/yonathan/active-topic"])
