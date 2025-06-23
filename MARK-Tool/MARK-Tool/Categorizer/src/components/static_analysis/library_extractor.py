import pandas as pd
import os

# dato il nome del file .py legge tutte le parole dopo import e ne restituisce una lista
# per qualeche motivo è utilizzata in consumer(CREDO SIA UN REFUSO TODO)
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

# dato un file .py e un dizionario(insieme delle librerire utilizzate dai producer o dai consumer) restiruisce una lista delle
#librerie trovate che apprtengono al dizionario.
# funzione utilizzata in producer_classifier_by_dic ma non in consumer(DA CAPIRE TODO).
def check_ml_library_usage(file, library_dict, is_consumer = False):
    file_libraries = get_libraries(file)
    for i in range(len(file_libraries)):
        if "." in file_libraries[i]:
            file_libraries[i] = file_libraries[i].split(".")[0]
        # solo il consumer
        if is_consumer:
            file_libraries[i] = file_libraries[i].replace("\n", "")
        #filter dict libraries from file libraries
    dict_libraries = library_dict[library_dict['library'].isin(file_libraries)]

    return dict_libraries