import os

#----------------------------------------------------------------------------------------------------------------------------
#TODO script mai utilizzato, ci sono gli import in consumer e producer ma non vengono mai utilizzati.
#TODO probabilmente un refuso, da chiedere.
#----------------------------------------------------------------------------------------------------------------------------


def convert_notebook_to_code( file):
    os.system(f"jupyter nbconvert --to script {file}")
    return file.replace('.ipynb', '.py')

def convert_and_check_notebook(file):
    os.system(f"jupyter nbconvert --to script {file}")
    file_py = file.replace('.ipynb','.py')
    if os.path.exists(file_py):
        return True
    return False

def convert_all_notebooks(folder_path):
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")

    converted_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ipynb'):
                full_path = os.path.join(root, file)
                try:
                    converted_file = convert_notebook_to_code(full_path)
                    converted_files.append(converted_file)
                    print(f"Converted: {full_path} -> {converted_file}")
                except Exception as e:
                    print(f"Error converting {full_path}: {e}")

    return converted_files

if __name__ == "__main__":
    folder_path = "../../../repos/repos2/"

    try:
        converted_files = convert_all_notebooks(folder_path)
        print("\nConversion completed.")
        print("Converted files:")
        for file in converted_files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")