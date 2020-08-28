#!/usr/bin/env python3
import json
from rofi import Rofi
import subprocess
from sys import argv

project_path = "/home/yonathan/active-topic/.project.json"

project = None
with open(project_path) as project_file:
    content = ""
    for line in project_file:
        content += line
    project = json.loads(content)

rofi = Rofi(rofi_args=["-i"])

options = list(project.keys())
index, key = rofi.select("Select a resource", options)

if index == -1:
    exit(0)

subprocess.Popen(project[options[index]],
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
