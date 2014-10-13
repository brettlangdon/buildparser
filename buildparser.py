__version__ = "0.1.0"

import os

PERMITTED_EXTENSIONS = ["yml", "json"]


def parse(directory=None, name="build"):
    if directory is None:
        directory = os.getcwd()
    else:
        directory = os.path.abspath(directory)

    dir_name = os.path.join(directory, ".%s" % (name, ))
    if os.path.exists(dir_name):
        return parse_directory(dir_name)

    for ext in PERMITTED_EXTENSIONS:
        file_name = os.path.join(directory, ".%s.%s" % (name, ext))
        if os.path.exists(file_name):
            return parse_file(file_name)


def parse_directory(dir_name):
    pass


def parse_file(file_name):
    pass
