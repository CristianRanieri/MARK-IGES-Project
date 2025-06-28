import os

class NotebookConverter:
    def __init__(self, folder_path="../../../repos/repos2/"):
        self.folder_path = folder_path

    def convert_notebook_to_code(self, file):
        os.system(f"jupyter nbconvert --to script {file}")
        return file.replace('.ipynb', '.py')

    def convert_all_notebooks(self):
        converted_files = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.ipynb'):
                    full_path = os.path.join(root, file)
                    try:
                        converted_file = self.convert_notebook_to_code(full_path)
                        converted_files.append(converted_file)
                        print(f"Converted: {full_path} -> {converted_file}")
                    except Exception as e:
                        print(f"Error converting {full_path}: {e}")
        return converted_files

    def run(self):
        if not os.path.isdir(self.folder_path):
            print(f"Error: The folder '{self.folder_path}' does not exist.")
            return

        try:
            converted_files = self.convert_all_notebooks()
            print("\nConversion completed.")
            print("Converted files:")
            for file in converted_files:
                print(file)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    converter = NotebookConverter()
    converter.run()