#!/usr/bin/env python3
"""
The entry point into the workflow automation
"""
from os import path
from sys import argv
from rofi import Rofi
from command import Command
from project import Project
from lecture import Lecture

PROJECTS = {
    "Temp Course": "/home/yonathan/Courses/Temp-Course/.project.json"
}

CURRENT_PROJECT_PATH = None
CURRENT_PROJECT = None


def set_current_from_link():
    global CURRENT_PROJECT, CURRENT_PROJECT_PATH
    CURRENT_PROJECT_PATH = "/home/yonathan/active-topic/.project.json"
    CURRENT_PROJECT = Project(CURRENT_PROJECT_PATH)


def choose_project():
    set_current_from_link()
    global CURRENT_PROJECT
    CURRENT_PROJECT.unlink_soft_link().execute()
    projects = list(PROJECTS.keys())
    rofi = Rofi(rofi_args=["-i"])
    index, _ = rofi.select("Project to work on", projects)
    if index == -1:
        return
    CURRENT_PROJECT_PATH = PROJECTS.get(projects[index])
    CURRENT_PROJECT = Project(CURRENT_PROJECT_PATH)
    CURRENT_PROJECT.create_soft_link().execute()


def rofi_list_lectures():
    lectures = CURRENT_PROJECT.course_info
    if not lectures:
        return
    lectures = lectures.get_lectures()
    lectures_str = [str(l) for l in lectures]

    rofi = Rofi(rofi_args=["-i"])
    index, key = rofi.select("Choose a lecture", lectures_str, key4=(
        'Super+o', "Open lecture in Zathura"), key5=('Super+e', "Open tex file in vim"), key6=("Super+n", "Create a new Lecture"))
    if index == -1:
        return

    if key == 4:
        lectures[index].view().execute()
    elif key == 5:
        lectures[index].edit().execute()
    else:
        rofi = Rofi(rofi_args=["-i"])
        title = rofi.text_entry("Title for lecture: ")
        lecture = Lecture.create_new(CURRENT_PROJECT_PATH, title)
        lecture.edit().execute()


if __name__ == "__main__":

    try:
        if len(argv) == 1:
            exit()
        if argv[1] == "choose":
            choose_project()

        if argv[1] == "rofi":
            set_current_from_link()
            rofi = Rofi(rofi_args=["-i"])
            options = ["Tmux", "Github", "Resources", "Lectures"]
            index, _ = rofi.select(
                CURRENT_PROJECT.project_name, options)
            if index == -1:
                exit(0)

            if index == 0:
                CURRENT_PROJECT.open_tmux_layout().execute()

            if index == 1:
                CURRENT_PROJECT.open_github().execute()

            if index == 2:
                CURRENT_PROJECT.open_resources_rofi().execute()

            if index == 3:
                rofi_list_lectures()

    except:
        exit()
