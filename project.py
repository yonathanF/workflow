"""
A model for a single project

A project is simply a directory with a .project.json file in it.
This enables it to provide some global functionalities that are similar
across different kinds of projects
"""
import json
from command import Command
from rofi import Rofi
from os import (path, walk)
from lecture import Lecture


class Course:
    """
    If the project is a course, we keep other relevant course related information here
    """

    def __init__(self, context_path, course_context):
        self.project_root, _ = path.split(context_path)

    def get_lectures(self):
        lectures = []
        for root, dir_names, file_names in walk(path.join(self.project_root, "lectures")):
            for name in file_names:
                if name.endswith(".tex") and not name.startswith("preamble"):
                    lectures.append(Lecture(path.join(root, name)))

        lectures.sort(key=lambda x: x.date, reverse=True)
        return lectures


class Project:
    def __init__(self, context_path):
        self.context_path = context_path
        self.context = json.load(open(context_path, 'r'))
        self.project_name = self.context.get("project name")
        self.tmux_name = self.context.get("tmux name")
        self.course_info = None if not self.context.get(
            "course info") else Course(context_path, self.context.get("course info"))
        self.github = self.context.get("github")
        self.other_resources = self.context.get("resources")

    def open_github(self):
        """
        Generates a command that can open the github page in a brave browser
        """
        return Command("brave", ["-new-window", self.github])

    def open_resources_rofi(self):
        """
        Generates a comman that opens a rofi window which contains all the resources
        this project provides
        """
        rofi = Rofi(rofi_args=["-i"])
        resources = list(self.other_resources.keys())
        index, _ = rofi.select("Select a resource", resources)
        if index == -1:
            return
        command, *args = self.other_resources.get(resources[index])
        return Command(command, args)

    def start_new_email(self):
        """
        Generates a command that uses xdg-open to open the default email client
        with the "to" field set to this projects email
        """
        pass

    def open_tmux_layout(self):
        """ Opens the projects tmuxp layout """
        if self.tmux_name:
            return Command("kitty", ["--detach", "--execute", "tmuxp", "load", self.tmux_name])

    def create_soft_link(self):
        """ Generates a command that creates a soft link of directory to active-topic.

        note: Also see unlink_soft_link below
        """
        project_root, _ = path.split(self.context_path)
        return Command("ln", ["-s", project_root, "/home/yonathan/active-topic"])

    def unlink_soft_link(self):
        """ Creates a command that removes the soft link, typically uses active-topic"""
        return Command("unlink", ["/home/yonathan/active-topic"])


if __name__ == "__main__":
    c = "/home/yonathan/Courses/Temp-Course/.project.json"

    p = Project(c)
    for l in p.course_info.get_lectures():
        print(str(l))
