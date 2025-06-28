import os
import re
import time
import pandas as pd
from abc import ABC, abstractmethod

class MLAnalyzerBase(ABC):
    def __init__(self, output_folder, analysis_type):
        self.output_folder = output_folder
        self.analysis_type = analysis_type

    def init_analysis_folder(self):
        analysis_path = os.path.join(self.output_folder, f"{self.analysis_type}_Analysis")
        if not os.path.exists(analysis_path):
            os.makedirs(analysis_path)

        # Definisci il nome del file in base al tipo di analisi
        if self.analysis_type.lower() == "producer":
            results_filename = 'results_first_step.csv'
        else:
            results_filename = 'results_consumer.csv'

        self.results_file = os.path.join(self.output_folder, results_filename)

        if not os.path.exists(self.results_file):
            df = pd.DataFrame(columns=[
                'ProjectName',
                f'Is ML {self.analysis_type.lower()}',
                "where",
                "keyword",
                "line_number"
            ])
            df.to_csv(self.results_file, index=False)
        else:
            df = pd.read_csv(self.results_file)
            backup_file = os.path.join(self.output_folder, f'results_backup_{int(time.time())}.csv')
            if not os.path.exists(backup_file):
                df.to_csv(backup_file, index=False)

    @staticmethod
    def build_regex_pattern(keyword: str):
        keyword = re.escape(keyword)
        keyword = keyword.replace(r"\ ", r"\\s*")
        return re.compile(keyword, re.IGNORECASE)

    @staticmethod
    def baseline_check(project: str, dir: str, df: pd.DataFrame):
        return f"{project}/{dir}" in df['ProjectName'].values

    @staticmethod
    def load_library_dict(input_file: str):
        return pd.read_csv(input_file, delimiter=",")

    @abstractmethod
    def check_training_method(self, file: str, library_dict_path: str):
        """
        Metodo astratto: deve essere implementato nelle classi figlie.
        Deve restituire tuple (libraries, keywords, ...)
        """
        pass
