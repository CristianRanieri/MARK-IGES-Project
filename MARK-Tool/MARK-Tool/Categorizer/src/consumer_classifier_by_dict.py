import os
import pandas as pd
import re
import time
import warnings
from components.static_analysis.library_extractor import check_ml_library_usage, get_libraries
from components.notebook_converter import convert_and_check_notebook
import logging

logging.basicConfig(level = logging.DEBUG)
class MLConsumerAnalyzer:
    def __init__(self, output_folder="Consumers/"):
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.init_consumer_analysis_folder()

    # TODO
    # non capisco perchè è stata reimplementata, in producer si utilizza direttamente quella implementata in library_exstractor.py
    def check_ml_library_usage(self,file, library_dict):
        file_libraries = get_libraries(file)
        for i in range(len(file_libraries)):
            if "." in file_libraries[i]:
                file_libraries[i] = file_libraries[i].split(".")[0]
            file_libraries[i] = file_libraries[i].replace("\n","")
        # filter dict libraries from file libraries
        dict_libraries = library_dict[library_dict['library'].isin(file_libraries)]

        return dict_libraries

    def init_consumer_analysis_folder(self):
        consumer_analysis_path = os.path.join(self.output_folder, "Consumer_Analysis")
        if not os.path.exists(consumer_analysis_path):
            os.makedirs(consumer_analysis_path)

        results_file = os.path.join(self.output_folder, 'results_consumer.csv')
        if not os.path.exists(results_file):
            df = pd.DataFrame(columns=['ProjectName', 'Is ML consumer', "where", "keyword", "line_number", "libraries"])
            df.to_csv(results_file, index=False)
        else:
            # Create a backup of existing results
            df = pd.read_csv(results_file)
            df.to_csv(os.path.join(self.output_folder, f'results_backup_{time.time()}.csv'), index=False)

    def check_training_method(self, file, producer_library):
        producer_library_dict = self.load_producer_library_dict(producer_library)
        producer_related_dict = self.check_ml_library_usage(file, producer_library_dict)
        producer_keywords = producer_related_dict['Keyword'].tolist()
        producer_library_dict_list = producer_related_dict['library'].tolist()

        if len(producer_library_dict_list) == 0:
            return False
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
            # check the presence of method that are producer
            if len(producer_library_dict_list) != 0:
                for keyword in producer_keywords:
                    if keyword in file_content:
                        return True
                return False
            return False

    def check_for_inference_method(self, file, consumer_library, producer_library, rules_3):
        list_keywords = []
        list_load_keywords = []

        # Load the consumer library dictionary dynamically
        consumer_library_dict = self.load_consumer_library_dict(consumer_library)
        consumer_related_dict = self.check_ml_library_usage(file, consumer_library_dict)
        consumer_keywords = consumer_related_dict['Keyword'].tolist()
        consumer_library_dict_list = consumer_related_dict['library'].tolist()

        flag = False
        # First, check if the

        # file uses ML libraries

        if len(consumer_library_dict_list) != 0:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        for keyword in consumer_keywords:
                            if '.' in str(keyword):
                                keyword = keyword.replace('.', '\.')
                            # Build regex to handle spaces within keywords
                            if '\s' in str(keyword):
                                parts = keyword.split()
                                regex = r'\s*'.join(parts)  # Allows optional spaces between parts of the keyword
                                pattern = re.compile(regex, re.IGNORECASE)
                            else:
                                if '(' in str(keyword):
                                    keyword = keyword.replace('(', '\(')
                                pattern = re.compile(str(keyword), re.IGNORECASE)
                            if re.search(pattern, line):
                                if rules_3:
                                    # here we have to check if the training is performed within the same file
                                    # get library of the keyword
                                    if self.check_training_method(file, producer_library):
                                        flag = False
                                    else:
                                        flag = True
                                else:
                                    flag = True

                            if flag:
                                keyword = keyword.replace("\\", "")

                                related_match = consumer_related_dict[consumer_related_dict['Keyword'] == keyword]

                                found_result = {
                                    'keyword': keyword,
                                    'library': related_match['library'].values[0],
                                    'file': file,
                                    'line': line.strip(),
                                    'line_number': line_number
                                }
                                list_keywords.append(found_result)
                                flag = False  # Reset flag for next iteration
            except UnicodeDecodeError:
                print(f"Error reading file {file}")
                return consumer_library_dict_list, list_keywords, list_load_keywords
            except FileNotFoundError:
                print(f"Error finding file {file}")
                return consumer_library_dict_list, list_keywords, list_load_keywords
        return consumer_library_dict_list, list_keywords, list_load_keywords


    def analyze_single_file(self, file, repo, consumer_library, producer_library, rules_3):
        keywords = []
        list_load_keywords = []
        libraries = []
        if file:
            libraries, keywords, list_load_keywords = self.check_for_inference_method(file, consumer_library, producer_library, rules_3)
            if len(keywords) > 0:
                print(f"Found {file} with ML libraries{libraries} and training instruction {keywords} in {repo}")
                return libraries, keywords, list_load_keywords, file
            return libraries, keywords, list_load_keywords, file
        return libraries, keywords, list_load_keywords, file

    def analyze_project_for_consumers(self, repo_contents, project, in_dir, consumer_library, producer_library, rules_3,rules_4):
        df = pd.DataFrame(columns=['ProjectName', 'Is ML consumer', 'libraries', "where", "keywords", 'line_number'])
        for root, dirs, files in os.walk(repo_contents):
            for file in files:
                if file.endswith(('.py','.ipynb')):
                    #added rule 4 conditions for ablations
                    if rules_4 and re.search(r"test|example|eval|validat", file, re.IGNORECASE):
                        continue
                    file_path = os.path.join(root, file)
                    libraries, keywords, list_load_keywords, file_path = self.analyze_single_file(file_path, repo_contents, consumer_library, producer_library, rules_3)
                    if keywords:
                        for keyword in keywords:
                            df = pd.concat([
                                df,
                                pd.DataFrame({
                                    'ProjectName': f'{project}/{in_dir}',
                                    'Is ML consumer': 'Yes',
                                    'libraries': keyword['library'],
                                    'where': file_path,
                                    'keywords': keyword['keyword'],
                                    'line_number': keyword['line_number']
                                }, index=[0])
                            ], ignore_index=True)
        output_file = os.path.join(self.output_folder, f'{project}_{in_dir}_ml_consumer.csv')
        if not df.empty:
            df.to_csv(output_file, index=False)
        return df

    def analyze_projects_set_for_consumers(self, input_folder, consumer_library, producer_library, rules_3, rules_4):
        results_file = os.path.join(self.output_folder, 'results_consumer.csv')
        df = pd.read_csv(results_file)

        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir in os.listdir(os.path.join(input_folder, project)):
                print("Project:", project)
                if os.path.isdir(os.path.join(input_folder, project, dir)):
                    new_df = self.analyze_project_for_consumers(
                        os.path.join(input_folder, project, dir),
                        project,
                        dir,
                        consumer_library, producer_library, rules_3, rules_4
                    )
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(results_file, index=False)

        return df

    @staticmethod
    def load_consumer_library_dict(input_file):
        return pd.read_csv(input_file, delimiter=",")

    @staticmethod
    def load_producer_library_dict(input_file):
        return pd.read_csv(input_file, delimiter=",")

    @staticmethod
    def baseline_check(project, dir, df):
        return f"{project}/{dir}" in df['ProjectName'].values

    @staticmethod
    def build_regex_pattern(keyword):
        keyword = re.escape(keyword)
        # Replace escaped spaces with regex pattern for optional whitespace
        keyword = keyword.replace(r"\ ", r"\\s*")

        return re.compile(keyword, re.IGNORECASE)

