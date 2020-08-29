"""
A model for a single project

A project is simply a directory with a .project.json file in it.
This enables it to provide some global functionalities that are similar
across different kinds of projects
"""
import json
from command import Command
from rofi import Rofi
from os import path


class Course:
    """
    If the project is a course, we keep other relevant course related information here
    """

    def __init__(self, context):
        pass


class Project:
    def __init__(self, context_path):
        self.context_path = context_path
        self.context = json.load(open(context_path, 'r'))
        self.project_name = self.context.get("project_name")
        self.course_info = [] if not self.context.get("course info") else Course(
            self.context.get("course info"))
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

    def create_soft_link(self):
        """ Generates a command that creates a soft link of directory to active-topic.

        note: Also see unlink_soft_link below
        """
        project_root, _ = path.split(self.context_path)
        return Command("ln", ["-s", project_root, "/home/yonathan/active-topic"])

    def unlink_soft_link(self):
        """ Creates a command that removes the soft link, typically uses active-topic"""
        return Command("unlink", ["/home/yonathan/active-topic"])
