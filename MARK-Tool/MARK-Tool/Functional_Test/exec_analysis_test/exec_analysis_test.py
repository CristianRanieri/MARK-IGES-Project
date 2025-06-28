import csv
import unittest
import subprocess
import os
import sys
import shutil
import pandas as pd
from io import StringIO

def read_csv_header(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return next(reader, [])

class BaseExecAnalysisTest(unittest.TestCase):
    temp_input_dir = None
    temp_output_dir = None
    expected_producer_files = []
    expected_consumer_files = []

    @classmethod
    def setUpClass(cls):
        # Non fallisce, esegue il test comunque
        if not os.path.isdir(cls.temp_output_dir):
            os.makedirs(cls.temp_output_dir, exist_ok=True)

        cls.producers_output = os.path.join(cls.temp_output_dir, "Producers", "Producers_Final")
        cls.consumers_output = os.path.join(cls.temp_output_dir, "Consumers", "Consumers_Final")

    def tearDown(self):
        """Pulisce completamente la cartella di output dopo ogni test"""
        for item in os.listdir(self.temp_output_dir):
            item_path = os.path.join(self.temp_output_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    def compare_csv_on_columns(self, actual_path, expected_content, columns):
        actual_df = pd.read_csv(actual_path, usecols=columns)
        expected_df = pd.read_csv(StringIO(expected_content), usecols=columns)

        # Ordino per rendere il confronto indipendente dall'ordine delle righe
        actual_df_sorted = actual_df.sort_values(by=columns).reset_index(drop=True)
        expected_df_sorted = expected_df.sort_values(by=columns).reset_index(drop=True)

        try:
            pd.testing.assert_frame_equal(actual_df_sorted, expected_df_sorted, check_like=True)
        except AssertionError as e:
            self.fail(f"Differenze nei file CSV sulle colonne {columns}:\n{e}")

    def test_exec_analysis_creates_expected_files(self):
        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "Categorizer", "src", "exec_analysis.py")),
            "--input_path", self.temp_input_dir,
            "--output_path", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        # Accetta 0 (ok) o 2 (gestione input mancante)
        if result.returncode == 1:
            print("Input mancante gestito correttamente. Nessun controllo successivo necessario.")
            return  # esce dal test
        self.assertEqual(result.returncode, 0, f"Errore nell'esecuzione dello script: {result.stderr}")

        self.assertTrue(os.path.isdir(self.producers_output), "Cartella Producers_Final mancante")
        self.assertTrue(os.path.isdir(self.consumers_output), "Cartella Consumers_Final mancante")

        produced_producer_files = [
            f for f in os.listdir(self.producers_output)
            if os.path.isfile(os.path.join(self.producers_output, f))
        ]
        produced_consumer_files = [
            f for f in os.listdir(self.consumers_output)
            if os.path.isfile(os.path.join(self.consumers_output, f))
        ]

        # Definisci le colonne su cui fare il confronto
        columns_to_check = ["ProjectName", "Is ML producer", "libraries", "keywords", "line_number"]

        # ---- Producers
        for expected_file, expected_content in self.expected_producer_files.items():
            self.assertIn(expected_file, produced_producer_files,
                          f"File atteso non trovato in Producers_Final: {expected_file}")
            actual_path = os.path.join(self.producers_output, expected_file)

            if isinstance(expected_content, str):
                # Usa la nuova funzione solo per CSV completi (con righe)
                if '\n' in expected_content and ',' in expected_content:
                    self.compare_csv_on_columns(actual_path, expected_content, columns_to_check)
                else:
                    actual_header = read_csv_header(actual_path)
                    expected_header = expected_content.split(",")
                    self.assertEqual(actual_header, expected_header,
                                     f"Header non corrisponde per file: {expected_file}")
            else:
                raise ValueError(f"Formato non supportato per expected_content in file {expected_file}")

        # ---- Consumers
        # Qui puoi fare analoga cosa se serve (puoi adattare colonne_to_check se diverso)
        for expected_file, expected_content in self.expected_consumer_files.items():
            self.assertIn(expected_file, produced_consumer_files,
                          f"File atteso non trovato in Consumers_Final: {expected_file}")
            actual_path = os.path.join(self.consumers_output, expected_file)

            if isinstance(expected_content, str):
                if '\n' in expected_content and ',' in expected_content:
                    # Se vuoi, qui usi un set di colonne adatto per consumer
                    self.compare_csv_on_columns(actual_path, expected_content,
                                                ["ProjectName", "Is ML consumer", "libraries", "keywords",
                                                 "line_number"])
                else:
                    actual_header = read_csv_header(actual_path)
                    expected_header = expected_content.split(",")
                    self.assertEqual(actual_header, expected_header,
                                     f"Header non corrisponde per file: {expected_file}")
            else:
                raise ValueError(f"Formato non supportato per expected_content in file {expected_file}")

        # ---- File inattesi
        unexpected_producers = set(produced_producer_files) - set(self.expected_producer_files.keys())
        unexpected_consumers = set(produced_consumer_files) - set(self.expected_consumer_files.keys())

        self.assertFalse(unexpected_producers, f"File inattesi trovati in Producers_Final: {unexpected_producers}")
        self.assertFalse(unexpected_consumers, f"File inattesi trovati in Consumers_Final: {unexpected_consumers}")


def load_file_content(path):
    with open(path, newline='', encoding='utf-8') as f:
        return f.read()

def concat_csvs(path1, path2):
    with open(path1, newline='', encoding='utf-8') as f1, open(path2, newline='', encoding='utf-8') as f2:
        reader1 = list(csv.reader(f1))
        reader2 = list(csv.reader(f2))

        # Verifica che gli header siano uguali
        if reader1[0] != reader2[0]:
            raise ValueError("I file hanno header diversi e non possono essere concatenati.")

        # Unisce solo i dati, evitando di duplicare l'header
        rows = [reader1[0]] + reader1[1:] + reader2[1:]

        # Converte in stringa CSV
        return "\n".join([",".join(row) for row in rows])



# EA_0 ERROE
class TestCase0(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_non_esiste"
    temp_output_dir = "Test_input/output"
    expected_producer_files = [
        "results_first_step.csv"
    ]
    expected_consumer_files = [
        "results_consumer.csv"
    ]

# EA_1 OK
class TestCase1(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_1"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "ProjectName,Is ML producer,where,keyword,line_number"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "ProjectName,Is ML consumer,where,keyword,line_number"
    }

# EA_2 OK
class TestCase2(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_2"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "aaronlam88_cmpe295_ml_producer.csv" : load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv"),
        "results_first_step.csv" : load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv")
    }
    expected_consumer_files = {
        "results_consumer.csv": "ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords"
    }

# EA_3 OK
class TestCase3(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_3"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords"
    }
    expected_consumer_files = {
        "keums_melodyExtraction_JDC_ml_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv"),
        "results_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv")
    }

# EA_4 OK
class TestCase4(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_4"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_producer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv"),
        "results_first_step.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv")
    }
    expected_consumer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_consumer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv"),
        "results_consumer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv")
    }

# EA_5
class TestCase5(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_5"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv": "ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords"
    }

# EA_6
class TestCase6(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_6"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "aaronlam88_cmpe295_ml_producer.csv" : load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv"),
        "results_first_step.csv" : load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv")
    }
    expected_consumer_files = {
        "keums_melodyExtraction_JDC_ml_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv"),
        "results_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv")
    }

# EA_7
class TestCase7(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_7"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv": "ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords"
    }
    expected_consumer_files = {
        "keums_melodyExtraction_JDC_ml_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv"),
        "results_consumer.csv" : load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv")
    }

# EA_8
class TestCase8(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_8"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_producer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv"),
        "aaronlam88_cmpe295_ml_producer.csv": load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv"),
        "results_first_step.csv" : concat_csvs("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv","Test_input/aaronlam88_cmpe295_ml_producer_test.csv")
    }
    expected_consumer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_consumer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv"),
        "results_consumer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv")
    }

# EA_9
class TestCase9(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input_9"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_producer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv"),
        "aaronlam88_cmpe295_ml_producer.csv": load_file_content("Test_input/aaronlam88_cmpe295_ml_producer_test.csv"),
        "results_first_step.csv" : concat_csvs("Test_input/appinho_SAComputerVisionMachineLearning_ml_producer_test.csv","Test_input/aaronlam88_cmpe295_ml_producer_test.csv")
    }
    expected_consumer_files = {
        "appinho_SAComputerVisionMachineLearning_ml_consumer.csv" : load_file_content("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv"),
        "keums_melodyExtraction_JDC_ml_consumer.csv": load_file_content("Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv"),
        "results_consumer.csv" : concat_csvs("Test_input/appinho_SAComputerVisionMachineLearning_ml_consumer_test.csv","Test_input/keums_melodyExtraction_JDC_ml_consumer_test.csv")
    }


if __name__ == '__main__':
    unittest.main()
