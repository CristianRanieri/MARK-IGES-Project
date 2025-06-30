import os
import pandas as pd
import re
import logging
import warnings
from components.static_analysis.library_extractor import LibraryAnalyzer
from analyzer_base import MLAnalyzerBase

warnings.simplefilter(action='ignore', category=FutureWarning)

logging.basicConfig(level=logging.DEBUG)

class MLProducerAnalyzer(MLAnalyzerBase):
    def __init__(self, output_folder="Producers/"):
        super().__init__(output_folder, analysis_type="Producer")
        self.init_analysis_folder()

    def check_training_method(self, file, library_dict_path):
        # Implementazione specifica producer
        producer_library_dict = self.load_library_dict(library_dict_path)
        list_keywords = []
        list_load_keywords = []
        library_analyzer = LibraryAnalyzer(file)

        producer_related_dict = library_analyzer.check_ml_library_usage(producer_library_dict)
        producer_keywords = producer_related_dict['Keyword'].tolist()
        producer_library_dict_list = producer_related_dict['library'].tolist()
        flag = False
        if len(producer_library_dict_list) != 0:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        line.replace("(", "\(")
                        for keyword in producer_keywords:
                            # Build regex to handle spaces within keywords
                            if '.' in str(keyword):
                                keyword = keyword.replace('.', '\.')
                            if '\s' in str(keyword):
                                parts = keyword.split()
                                regex = r'\s*'.join(parts)  # Allows optional spaces between parts of the keyword
                                pattern = re.compile(regex, re.IGNORECASE)
                            else:
                                if '(' in str(keyword):
                                    keyword = keyword.replace('(', '\(')
                                pattern = re.compile(str(keyword), re.IGNORECASE)

                            if re.search(pattern, line):
                                flag = True
                                keyword = keyword.replace("\\", "")

                                related_match = producer_related_dict[producer_related_dict['Keyword'] == keyword]

                                found_result = {
                                    'keyword': keyword,
                                    'library': related_match['library'].values[0],
                                    'file': file,
                                    'line': line.strip(),
                                    'line_number': line_number
                                }
                                list_keywords.append(found_result)
                            if flag:
                                flag = False  # Reset flag for next iteration
            except UnicodeDecodeError:
                print(f"Error reading file {file}")
                return producer_library_dict_list, list_keywords, list_load_keywords
            except FileNotFoundError:
                print(f"Error finding file {file}")
                return producer_library_dict_list, list_keywords, list_load_keywords

        return producer_library_dict_list, list_keywords, list_load_keywords

    def analyze_single_file(self, file, repo, library_dict_path):
        keywords = []
        libraries = []
        if file:
            libraries, keywords, list_load_keywords = self.check_training_method(file, library_dict_path)
            if len(keywords) > 0:
                print(f"Found {file} with ML libraries{libraries} and training instruction {keywords} in {repo}")
                return libraries, keywords, file
            return libraries, keywords, file
        return libraries, keywords, file

    def analyze_project_for_producers(self, repo_contents, project, dir, library_dict_path):
        df = pd.DataFrame(columns=['ProjectName', 'Is ML producer', 'libraries', "where", "keywords", 'line_number'])
        for root, dirs, files in os.walk(repo_contents):
            for file in files:
                if file.endswith(('.py','ipynb')):
                    file_path = os.path.join(root, file)
                    libraries, keywords, file_path = self.analyze_single_file(file_path, repo_contents, library_dict_path)
                    if keywords:
                        for keyword in keywords:
                            df = pd.concat([
                                df,
                                pd.DataFrame({
                                    'ProjectName': f'{project}/{dir}',
                                    'Is ML producer': 'Yes',
                                    'libraries': keyword['library'],
                                    'where': file_path,
                                    'keywords': keyword['keyword'],
                                    'line_number': keyword['line_number']
                                }, index=[0])
                            ], ignore_index=True)
        output_file = os.path.join(self.output_folder, f'{project}_{dir}_ml_producer.csv')
        if not df.empty:
            df.to_csv(output_file, index=False)
        return df

    def analyze_projects_set_for_producers(self, input_folder, library_dict_path):
        results_file = os.path.join(self.output_folder, 'results_first_step.csv')
        df = pd.read_csv(results_file)

        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir in os.listdir(os.path.join(input_folder, project)):
                print("Project:", project)
                if os.path.isdir(os.path.join(input_folder, project, dir)):
                    if not self.baseline_check(project, dir, df):
                        new_df = self.analyze_project_for_producers(
                            os.path.join(input_folder, project, dir),
                            project,
                            dir,
                            library_dict_path
                        )
                        df = pd.concat([df, new_df], ignore_index=True)
                        df.to_csv(results_file, index=False)

        return df
