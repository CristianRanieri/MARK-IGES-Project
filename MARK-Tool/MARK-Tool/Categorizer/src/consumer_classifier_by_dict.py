import os
import pandas as pd
import re
from components.static_analysis.library_extractor import check_ml_library_usage
import logging
from analyzer_base import MLAnalyzerBase

logging.basicConfig(level = logging.DEBUG)
class MLConsumerAnalyzer(MLAnalyzerBase):
    def __init__(self, output_folder="Consumers/"):
        super().__init__(output_folder, analysis_type="Consumer")
        self.init_analysis_folder()

    def check_training_method(self, file, producer_library):
        # Implementazione specifica consumer
        producer_library_dict = self.load_library_dict(producer_library)
        producer_related_dict = check_ml_library_usage(file, producer_library_dict, True)
        producer_keywords = producer_related_dict['Keyword'].tolist()
        producer_library_dict_list = producer_related_dict['library'].tolist()

        if len(producer_library_dict_list) == 0:
            return False

        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
            for keyword in producer_keywords:
                if keyword in file_content:
                    return True
            return False

    def check_for_inference_method(self, file, consumer_library, producer_library, rules_3):
        list_keywords = []
        list_load_keywords = []

        consumer_library_dict = self.load_library_dict(consumer_library)
        consumer_related_dict = check_ml_library_usage(file, consumer_library_dict, True)
        consumer_keywords = consumer_related_dict['Keyword'].tolist()
        consumer_library_dict_list = consumer_related_dict['library'].tolist()

        flag = False

        if len(consumer_library_dict_list) != 0:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        for keyword in consumer_keywords:
                            pattern = self.build_regex_pattern(keyword)
                            if re.search(pattern, line):
                                if rules_3:
                                    if self.check_training_method(file, producer_library):
                                        flag = False
                                    else:
                                        flag = True
                                else:
                                    flag = True

                            if flag:
                                keyword_clean = keyword.replace("\\", "")
                                related_match = consumer_related_dict[consumer_related_dict['Keyword'] == keyword]

                                found_result = {
                                    'keyword': keyword_clean,
                                    'library': related_match['library'].values[0],
                                    'file': file,
                                    'line': line.strip(),
                                    'line_number': line_number
                                }
                                list_keywords.append(found_result)
                                flag = False
            except (UnicodeDecodeError, FileNotFoundError) as e:
                logging.warning(f"Error reading file {file}: {e}")
                return consumer_library_dict_list, list_keywords, list_load_keywords

        return consumer_library_dict_list, list_keywords, list_load_keywords

    def analyze_single_file(self, file, repo, consumer_library, producer_library, rules_3):
        keywords = []
        list_load_keywords = []
        libraries = []
        if file:
            libraries, keywords, list_load_keywords = self.check_for_inference_method(file, consumer_library, producer_library, rules_3)
            if len(keywords) > 0:
                logging.info(f"Found {file} with ML libraries {libraries} and training instruction {keywords} in {repo}")
            return libraries, keywords, list_load_keywords, file
        return libraries, keywords, list_load_keywords, file

    def analyze_project_for_consumers(self, repo_contents, project, in_dir, consumer_library, producer_library, rules_3, rules_4):
        df = pd.DataFrame(columns=['ProjectName', 'Is ML consumer', 'libraries', "where", "keywords", 'line_number'])
        for root, dirs, files in os.walk(repo_contents):
            for file in files:
                if file.endswith(('.py', '.ipynb')):
                    if rules_4 and re.search(r"test|example|eval|validat", file, re.IGNORECASE):
                        continue
                    file_path = os.path.join(root, file)
                    libraries, keywords, list_load_keywords, file_path = self.analyze_single_file(
                        file_path, repo_contents, consumer_library, producer_library, rules_3)
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
        df = pd.read_csv(self.results_file)

        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir in os.listdir(os.path.join(input_folder, project)):
                logging.info(f"Project: {project}")
                if os.path.isdir(os.path.join(input_folder, project, dir)):
                    new_df = self.analyze_project_for_consumers(
                        os.path.join(input_folder, project, dir),
                        project,
                        dir,
                        consumer_library, producer_library, rules_3, rules_4
                    )
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(self.results_file, index=False)

        return df