#!/usr/bin/env python3
from rofi import Rofi
import os
import re
from datetime import datetime
import subprocess

base_path = "/home/yonathan/active-topic/"


titles_to_path = {}
lectures = []
regex = r"\{\s*(.*)\s*\}"
p = re.compile(regex)
for root, dir_names, file_names in os.walk(os.path.join(base_path, "lectures")):
    for name in file_names:
        if name.endswith(".tex"):
            with open(os.path.join(root, name), "r") as tex_file:
                current_lecture = []
                current_lecture.append(os.path.join(root, name))
                lines = tex_file.readlines()
                for line in lines:
                    if "LectureTitle" in line:
                        match = p.findall(line)
                        if match:
                            match = match[0].strip()
                            current_lecture.append(match)
                    if "LectureDate" in line:
                        match = p.findall(line)
                        if match:
                            match = datetime.strptime(
                                match[0].strip(), '%d  %B %Y')
                            current_lecture.append(match)
                lectures.append(current_lecture)

lectures = sorted(lectures, key=lambda x: x[1], reverse=True)
i = len(lectures)
lectures_clean = []
for lecture in lectures:
    lectures_clean.append(
        str(i)+": "+lecture[2]+" (" + lecture[1].strftime('%d %B')+")")
    i -= 1

r = Rofi(rofi_args=["-i"])
index, key = r.select("Select a lecture", lectures_clean)
if index != -1:
    subprocess.Popen(["zathura", lectures[index][0][:-3]+"pdf"])
