import os
import shutil
import errno

"""
Program Created folders per Year & Month.
File must be formatted as YY-MM-DD
file_format allows any file type to be organised.
DEFAULT file_format is a text file (.txt)
"""


def File_Date_Organiser(file_format=".txt"):

    for number, file in enumerate(os.listdir()):

        if file.endswith(file_format):
            print(file)
            try:
                os.mkdir("{}-{}".format(file[:2], file[3:5]))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise exc

            shutil.move(file, "{}-{}".format(file[:2], file[3:5]))


File_Date_Organiser()
