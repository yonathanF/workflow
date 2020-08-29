"""
A command object. Simply hides the execution of the commands
and pushes out the actual execution to the edge. Basically
same idea as passing a function to a higher order function
"""

import subprocess


class Command:
    def __init__(self, program, arguments):
        self.program = program
        self.arguments = arguments

    def execute(self):
        command = [self.program]
        command.extend(self.arguments)
        # subprocess.Popen(command, stdout=subprocess.PIPE)

        subprocess.Popen(command, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
