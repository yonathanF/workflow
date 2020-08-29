"""
Parser and lecture model. Basically builds lecture objects out of a list of file paths
"""

import pystache
import json
from os import path
from command import Command


class LectureParser:
    pass


class LectureFileBuilder:
    def __init__(self, lecture_title, context_path):
        with open(context_path, "r") as context_file:
            self.context = json.load(context_file)
        course_context = self.context["course info"]
        self.context_path = context_path
        self.lecture_number = course_context.get("lecture number")
        self.professor = course_context.get("professor")
        self.lecture_title = lecture_title
        self.course_name = course_context.get("course name")
        self.file_name = str(self.lecture_number) + "_" + \
            self.lecture_title.replace(" ", "_") + ".tex"

    def lecture_number(self):
        return self.lecture_number

    def professor(self):
        return self.professor

    def course_name(self):
        return self.course_name

    def lecture_title(self):
        return self.lecture_title

    def create_document(self):

        renderer = pystache.Renderer(file_extension="tex")
        self.context["course info"]["lecture number"] += 1
        json.dump(self.context, open(self.context_path, "w"))

        return renderer.render(self)

    def write_to_file(self):
        file_path = path.split(self.context_path)[0]
        file_path = path.join(file_path, "lectures", self.file_name)
        with open(file_path, 'w') as document_file:
            document_file.write(self.create_document())

        return file_path


class Lecture:
    """
    A model of lectures. It provides a means of editing, and searching lecture files
    """

    def __init__(self, latex_file_path):
        self.file_path = latex_file_path

    def form_pdf_path(self):
        return self.file_path[:-4] + ".pdf"

    def view(self):
        """Opens the pdf of this lecture in zathura"""
        return Command("zathura", [self.form_pdf_path()])

    def edit(self):
        """Returns a command that opens this lecture in vim"""
        directory = path.split(self.file_path)[0]
        return Command("kitty", ["--detach", "--directory", directory, "--execute", "nvim", self.file_path])

    def compile(self):
        """Returns a command that compiles the lecture"""

        directory, file = path.split(self.file_path)
        # TODO this seems to work in shell but it doesn't work from python
        return Command("latexmk", ["-pdf", self.file_path])

    @ classmethod
    def create_new(cls, context_path, title):
        """Creates a new latex file for the lecture based on the course info context
        :returns: Lecture
        """
        lecture_builder = LectureFileBuilder(title, context_path)
        file_path = lecture_builder.write_to_file()
        return Lecture(file_path)


if __name__ == "__main__":
    path_to_context = "/home/yonathan/Courses/Temp-Course/.project.json"

    lecture = Lecture.create_new(path_to_context, "Introductions")
    # lecture.edit().execute()
    # lecture.view().execute()
    # lecture.compile().execute()
