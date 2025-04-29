import pandas as pd
import os

def get_libraries(file):
    libraries = []
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(file, "r", encoding="ISO-8859-1") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print(f"Error reading file {file}")
            return libraries
    except FileNotFoundError:
        print(f"Error finding file {file}")
        return libraries

    # Your analysis logic here
    for line in lines:
        #delete trailing whitespaces at start if present
        line = line.lstrip()
        if 'import ' in line:
            if "from" in line:
                libraries.append(line.split(' ')[1])
            else:
                libraries.append(line.split(' ')[1])
    return libraries


def check_ml_library_usage(file, library_dict):
    file_libraries = get_libraries(file)
    for i in range(len(file_libraries)):
        if "." in file_libraries[i]:
            file_libraries[i] = file_libraries[i].split(".")[0]
    #filter dict libraries from file libraries
    dict_libraries = library_dict[library_dict['library'].isin(file_libraries)]

    return dict_libraries