import unittest
import subprocess
import os
import sys
import shutil

class BaseExecAnalysisTest(unittest.TestCase):
    temp_input_dir = None
    temp_output_dir = None
    expected_producer_files = []
    expected_consumer_files = []

    @classmethod
    def setUpClass(cls):
        assert os.path.isdir(cls.temp_input_dir), f"Input path non valido: {cls.temp_input_dir}"
        assert os.path.isdir(cls.temp_output_dir), f"Output path non valido: {cls.temp_output_dir}"

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

    def test_exec_analysis_creates_expected_files(self):
        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "Categorizer", "src", "exec_analysis.py")),
            "--input_path", self.temp_input_dir,
            "--output_path", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Errore nell'esecuzione dello script: {result.stderr}")

        self.assertTrue(os.path.isdir(self.producers_output), "Cartella Producers_Final mancante")
        self.assertTrue(os.path.isdir(self.consumers_output), "Cartella Consumers_Final mancante")

        produced_producer_files = os.listdir(self.producers_output)
        produced_consumer_files = os.listdir(self.consumers_output)

        for expected_file in self.expected_producer_files:
            self.assertIn(expected_file, produced_producer_files, f"File atteso non trovato in Producers_Final: {expected_file}")

        for expected_file in self.expected_consumer_files:
            self.assertIn(expected_file, produced_consumer_files, f"File atteso non trovato in Consumers_Final: {expected_file}")


# 0 elementi
class TestCase0(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input"
    temp_output_dir = "Test_input/output"
    expected_producer_files = [
        "921kiyo_3d-dl_ml_producer.csv",
        "results_first_step.csv"
    ]
    expected_consumer_files = [
        "921kiyo_3d-dl_ml_consumer.csv",
        "results_consumer.csv"
    ]

# 1 elemento sia producer che consumer
class TestCase1(BaseExecAnalysisTest):
    temp_input_dir = "Test_input/input"
    temp_output_dir = "Test_input/output"
    expected_producer_files = [
        "921kiyo_3d-dl_ml_producer.csv",
        "results_first_step.csv"
    ]
    expected_consumer_files = [
        "921kiyo_3d-dl_ml_consumer.csv",
        "results_consumer.csv"
    ]

# 1 consumer
class TestCase2(BaseExecAnalysisTest):
    temp_input_dir = "/path/assoluto/input_2"
    temp_output_dir = "/path/assoluto/output2"
    expected_producer_files = [
        "producers_result_A.csv"
    ]
    expected_consumer_files = [
        "consumers_result_A.csv",
        "consumers_result_B.csv"
    ]

# 1 producer
class TestCase3(BaseExecAnalysisTest):
    temp_input_dir = "/path/assoluto/input_2"
    temp_output_dir = "/path/assoluto/output2"
    expected_producer_files = [
        "producers_result_A.csv"
    ]
    expected_consumer_files = [
        "consumers_result_A.csv",
        "consumers_result_B.csv"
    ]

# 1 nessuno
class TestCase4(BaseExecAnalysisTest):
    temp_input_dir = "/path/assoluto/input_2"
    temp_output_dir = "/path/assoluto/output2"
    expected_producer_files = [
        "producers_result_A.csv"
    ]
    expected_consumer_files = [
        "consumers_result_A.csv",
        "consumers_result_B.csv"
    ]

# multipli elementi

if __name__ == '__main__':
    unittest.main()
